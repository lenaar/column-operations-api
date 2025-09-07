# API Key Security Migration - Case Study Response

## Current State Analysis

### Problems with Current Implementation

- **Security Risk**: API keys stored as plain text in `User.api_key` field
- **Limited Functionality**: Only one API key per user
- **No Audit Trail**: No tracking of key usage, creation, or revocation
- **No Expiration**: Keys never expire, creating long-term security exposure

### Production Impact

- Multiple users actively using API keys in production
- Zero downtime requirement for migration
- Backward compatibility must be maintained

## Proposed New Model

### 1. New Database Schema

```sql
-- New API Keys table
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    key_name VARCHAR(100) NOT NULL, -- User-friendly name for the key
    key_hash VARCHAR(255) NOT NULL, -- SHA-256 hash of the actual key
    key_prefix VARCHAR(20) NOT NULL, -- First 8 chars for identification (e.g., "ak_12345678")
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP NULL,
    expires_at TIMESTAMP NULL, -- Optional expiration
    is_active BOOLEAN DEFAULT TRUE,
    permissions JSONB DEFAULT '{}', -- Future: granular permissions
    metadata JSONB DEFAULT '{}' -- Additional key metadata
);

-- Indexes for performance
CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX idx_api_keys_hash ON api_keys(key_hash);
CREATE INDEX idx_api_keys_prefix ON api_keys(key_prefix);
CREATE INDEX idx_api_keys_active ON api_keys(is_active) WHERE is_active = TRUE;
```

### 2. Key Generation Strategy

```python
# Key format: ak_<prefix>_<random_32_chars>
# Example: ak_12345678_abcdef1234567890abcdef1234567890
def generate_api_key():
    prefix = generate_random_prefix(8)  # "12345678"
    secret = generate_random_secret(32)  # 32 random hex chars
    full_key = f"ak_{prefix}_{secret}"

    return {
        'full_key': full_key,
        'prefix': f"ak_{prefix}",
        'hash': sha256(full_key.encode()).hexdigest()
    }
```

## Migration Strategy Options

### Option 1: Migration Tracking Table (Recommended)

#### **Advantages:**

- **No User Model Changes**: No need to alter existing `users` table
- **Easy Cleanup**: Can be dropped after migration is complete
- **Comprehensive Tracking**: Full audit trail of migration process
- **Resume Capability**: Can restart from any point if script fails
- **Error Analysis**: Detailed error tracking and categorization

#### **Implementation:**

```sql
-- Migration tracking table
CREATE TABLE migration_tracking (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    legacy_key_hash VARCHAR(255) NOT NULL,
    new_key_id UUID REFERENCES api_keys(id),
    migration_status VARCHAR(20) NOT NULL, -- 'pending', 'completed', 'failed', 'skipped'
    error_reason TEXT NULL,
    migrated_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_migration_tracking_user_id ON migration_tracking(user_id);
CREATE INDEX idx_migration_tracking_status ON migration_tracking(migration_status);
```

#### **Migration Process:**

- **Check existing keys**: Determine if user already has new keys created during migration
- **Handle users with new keys**: Still migrate legacy key for backward compatibility (new keys stay in api_keys table)
- **Handle users without new keys**: Create first migrated key from legacy key
- **Duplicate prevention**: Check if legacy key already exists in new table
- **Key creation**: Create migrated key with same hash as legacy key
- **Tracking**: Record legacy key migration status in migration_tracking table (new keys don't need tracking)
- **Error handling**: Log failures with detailed error reasons
- **Return status**: Provide completion status and new key ID

### **User States During Migration**

#### **State 1: User with Only Legacy Key**

```python
# User has legacy key in users.api_key, no new keys
user_state = {
    'legacy_key': 'ak_1234567890abcdef',
    'new_keys': [],
    'migration_status': 'pending'
}

# Authentication: Uses legacy key
# New key creation: Goes to new table
# Migration: Creates migrated key in new table
```

#### **State 2: Dual-read, New-write (Legacy + New Keys)**

Release the backend change that switches writes for new keys to the new storage.

**Writes**: All newly created keys are stored only in the `api_keys` table.

**Reads**: Authentication checks both sources—first `api_keys` table, then the soon-to-be-legacy `users.api_key`.
This lets us keep serving traffic while the migration runs, without worrying about keys created during the process.

New users: Create the user with `api_key = NULL`, and create their keys in `api_keys` table with a safely hashed secret.

### Option 2: User Model Flags (Alternative)

#### **Advantages:**

- **Simpler Schema**: No additional tables needed
- **Direct User Tracking**: Migration status directly on user record

#### **Disadvantages:**

- **User Model Changes**: Requires altering existing `users` table
- **Migration Complexity**: Need to add new columns to existing table
- **Cleanup Required**: Must remove columns after migration
- **Less Flexible**: Harder to track detailed migration information

### Option 3: Null Password Approach (Not Recommended)

#### **Why This is Less Safe:**

- **Security Risk**: Setting `api_key` to NULL before migration is complete
- **Service Disruption**: Users lose access during migration window
- **Data Loss Risk**: If migration fails, users lose their keys permanently
- **No Rollback**: Cannot easily revert if issues occur

## Recommended Migration Plan

### Phase 1: Preparation (Zero Downtime)

**Duration**: 1-2 weeks

1. **Deploy New Schema**

   - Add new `api_keys` table alongside existing `User.api_key`
   - Deploy code changes to support both old and new authentication
   - No changes to existing API key validation logic

2. **Dual Authentication Support**

   ```python
   def authenticate_api_request(request):
       # Try new format first
       if new_key := extract_new_format_key(request):
           return authenticate_new_key(new_key)

       # Fallback to legacy format
       if legacy_key := extract_legacy_key(request):
           return authenticate_legacy_key(legacy_key)

       return None
   ```

3. **New Key Creation (Only New Table)**

   ```python
   class APIKeyService:
       @staticmethod
       def create_new_api_key(user_id: int, key_name: str) -> Dict[str, str]:
           """Create new API key - ONLY saves to new table"""
           key_data = generate_api_key()

           new_key = APIKey(
               user_id=user_id,
               key_name=key_name,
               key_hash=key_data['hash'],
               key_prefix=key_data['prefix'],
               created_at=datetime.utcnow()
           )

           db.session.add(new_key)
           db.session.commit()

           return {
               'key_id': new_key.id,
               'full_key': key_data['full_key'],
               'key_prefix': key_data['prefix']
           }
   ```

4. **Migration Tracking Setup**
   - Create `migration_tracking` table (only tracks legacy key migration)
   - Set up monitoring and logging
   - Prepare migration scripts

### Phase 2: User Migration (Gradual)

**Duration**: 2-4 weeks

1. **Frontend Updates**

   - Add new API key management interface
   - Allow users to create multiple named keys
   - Show migration status and encourage key rotation

2. **Migration API Endpoints**

   ```python
   # New endpoints for key management
   POST /api/v1/keys                    # Create new key in new table
   GET  /api/v1/keys                    # List user's keys, read from legacy and new table
   PUT  /api/v1/keys/{key_id}           # Update key (name, expiration), if migrated then update in the new table
   DELETE /api/v1/keys/{key_id}         # Revoke key, if migrated then update in the new table.
   POST /api/v1/keys/migrate            # Migrate legacy key to new format
   ```

   Update/Delete operations are dangerous if they are written to existing api key in the User table, consider a short lock duration while migration of row.

3. **Background Migration Process**
   - Run migration script with pagination (only migrates legacy keys)
   - Track progress in `migration_tracking` table (new keys don't need tracking)
   - Handle errors gracefully with detailed logging
   - Resume capability if script fails from the latest migrated, check for duplicates if exists go to next one.

### Phase 3: Legacy Key Migration (Automated)

**Duration**: 1-2 weeks

1. **Automated Migration Script**

   ```python
   def run_migration_with_tracking():
       """Run migration with comprehensive tracking - only migrates legacy keys"""
       total_users = get_users_with_legacy_keys()
       batch_size = 100

       for offset in range(0, total_users, batch_size):
           batch = get_migration_batch(offset, batch_size)

           for user in batch:
               result = migrate_user_key(user)  # Only migrates legacy key

               # Track legacy key migration in migration_tracking table
               record_migration_result(user['id'], result)

               if result['status'] == 'failed':
                   log_error_details(user['id'], result['error'])
   ```

2. **Error Handling and Resolution**

   - Categorize errors by type
   - Retry failed migrations
   - Manual resolution for complex cases
   - Comprehensive error reporting

3. **Monitoring During Migration**
   - Track migration progress in real-time
   - Monitor API error rates
   - Alert on failed migrations

### Phase 4: Legacy Deprecation (Controlled)

**Duration**: 4-6 weeks

1. **Final Cleanup**

   - Remove legacy authentication code
   - Drop `User.api_key` column
   - **Drop `migration_tracking` table** (easy cleanup - only tracked legacy key migration!)
   - Archive migration logs

2. **Rollback Strategy**
   - Keep legacy authentication code until migration complete
   - Ability to revert to legacy-only authentication
   - Data integrity checks before cleanup

### **Cleanup After Migration**

```sql
-- After migration is complete and verified
DROP TABLE migration_tracking;
-- That's it! Clean and simple.
-- Note: New keys created during migration stay in api_keys table (no cleanup needed)
```

## Timeline Summary

| Phase       | Duration       | Key Activities                        |
| ----------- | -------------- | ------------------------------------- |
| **Phase 1** | 1-2 weeks      | Schema deployment, dual auth support  |
| **Phase 2** | 2-4 weeks      | User migration, new UI, communication |
| **Phase 3** | 1-2 weeks      | Automated legacy key migration        |
| **Phase 4** | 4-6 weeks      | Legacy deprecation and cleanup        |
| **Total**   | **8-14 weeks** | Complete migration with zero downtime |
