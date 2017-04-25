DECLARE
    v_tag_id tags.tagid%type;
    v_random_postid posts.postid%type;
BEGIN
    SELECT tagid INTO v_tag_id FROM tags WHERE lower(name) like 'computer science';
    DBMS_OUTPUT.PUT_LINE(v_tag_id);
    FOR i IN 1..100 LOOP
        SELECT postid into v_random_postid
        FROM (
            SELECT postid
            FROM posts
            ORDER BY DBMS_RANDOM.RANDOM)
        WHERE rownum = 1;
        INSERT INTO posts_tags (postid, tagid) VALUES (v_random_postid, v_tag_id);
    END LOOP;
END;