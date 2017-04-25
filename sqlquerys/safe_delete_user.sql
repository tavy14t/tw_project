CREATE OR REPLACE PROCEDURE safe_delete_user(deleted_user_id int) AS
   v_ghost_user_id int;
BEGIN
   SELECT userid
       INTO v_ghost_user_id
       FROM users
       WHERE email='NoName';
   UPDATE comments
       SET userid=v_ghost_user_id
       WHERE userid=deleted_user_id;
   UPDATE posts
       SET userid=v_ghost_user_id
       WHERE userid=deleted_user_id;
   UPDATE users_tags
       SET userid=v_ghost_user_id
       WHERE userid=deleted_user_id;
   DELETE
       FROM users
       WHERE userid = deleted_user_id;
END;