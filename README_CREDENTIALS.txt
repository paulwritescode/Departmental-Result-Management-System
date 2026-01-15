================================================================================
                    IMPORTANT: CREDENTIALS LOCATION
================================================================================

For security reasons, all default test credentials have been moved to:

    📄 CREDENTIALS.md

This file is excluded from version control (.gitignore) to prevent accidental
exposure of sensitive information.

--------------------------------------------------------------------------------

WHERE TO FIND LOGIN CREDENTIALS:

1. Check CREDENTIALS.md in your local directory
2. Run: python3 setup_users.py (prints credentials during user creation)
3. Check SECURITY_NOTES.md for password change instructions

--------------------------------------------------------------------------------

PRODUCTION DEPLOYMENT WARNING:

⚠️  The default credentials in CREDENTIALS.md are for TESTING ONLY!

Before deploying to production:
✓ Change all default passwords
✓ Update SECRET_KEY (already done)
✓ Migrate to PostgreSQL
✓ Enable HTTPS
✓ Review SECURITY_NOTES.md

--------------------------------------------------------------------------------

FILES EXCLUDED FROM VERSION CONTROL:

- CREDENTIALS.md (contains test credentials)
- *.db (database files)
- .env (environment variables)

These files are listed in .gitignore and will NOT be committed to Git.

================================================================================
