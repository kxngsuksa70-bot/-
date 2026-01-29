-- Check teacher profile_picture values
SELECT id, username, name, profile_picture 
FROM teachers 
WHERE id = 1;

-- This will show what's currently stored in the database
-- Expected: https://hbbqwcesmwqnfgkmdayp.supabase.co/storage/v1/object/public/profile-pictures/teacher_1_...
-- If it's a local path like "teacher_1_.PNG", that's the problem
