set serveroutput on;

CREATE OR REPLACE PACKAGE populare_comentarii AS
    TYPE adjective_list_type IS TABLE OF VARCHAR2(64);
    adjective_list adjective_list_type;
    adjective_list_size INT;
    PROCEDURE fill_adjective_list;
    FUNCTION create_comment_text RETURN VARCHAR2;
    FUNCTION get_random_user_id RETURN users.userid%type;
    FUNCTION get_random_post_id RETURN posts.postid%type;
    PROCEDURE populate;
END populare_comentarii;
/

CREATE OR REPLACE PACKAGE BODY populare_comentarii AS
    PROCEDURE fill_adjective_list AS
    BEGIN
        adjective_list := adjective_list_type(
            'abandoned', 
            'awkward', 
            'babyish', 
            'buzzing', 
            'calculating', 
            'cylindrical', 
            'damaged', 
            'dutiful', 
            'each', 
            'extra-small', 
            'fabulous', 
            'fuzzy', 
            'gargantuan', 
            'gummy', 
            'hairy', 
            'half', 
            'icky', 
            'itchy', 
            'jaded', 
            'juvenile', 
            'kaleidoscopic', 
            'kosher', 
            'lame', 
            'luxurious', 
            'mad', 
            'mysterious', 
            'naive', 
            'nutty', 
            'obedient', 
            'overlooked', 
            'palatable', 
            'puzzling', 
            'quaint', 
            'quizzical', 
            'radiant', 
            'rusty', 
            'sad', 
            'sympathetic', 
            'tall', 
            'twin', 
            'ugly', 
            'utter', 
            'vacant', 
            'voluminous', 
            'wan', 
            'wow', 
            'yawning', 
            'yearly', 
            'zany', 
            'zealous');
        adjective_list_size := adjective_list.COUNT;
    END;
    
    FUNCTION create_comment_text RETURN VARCHAR2 AS
        v_actual_comment VARCHAR2(512);
        v_number_of_adjectives_per_com int;
        v_random_comment_number int;
    BEGIN
        v_random_comment_number := DBMS_RANDOM.VALUE(1, adjective_list_size);
        v_actual_comment := adjective_list(v_random_comment_number);
        v_number_of_adjectives_per_com := DBMS_RANDOM.VALUE(1, 10) - 1;
        FOR i in 1..v_number_of_adjectives_per_com LOOP
            v_random_comment_number := DBMS_RANDOM.VALUE(1, adjective_list_size);
            v_actual_comment := v_actual_comment || ', ' || adjective_list(v_random_comment_number);
        END LOOP;
        return v_actual_comment;
    END;
    
    FUNCTION get_random_user_id RETURN users.userid%type AS
        v_random_userid int;
    BEGIN
        SELECT userid into v_random_userid
        FROM (
            SELECT userid
            FROM users
            ORDER BY DBMS_RANDOM.RANDOM)
        WHERE  rownum = 1;
        return v_random_userid;
    END;
    
    FUNCTION get_random_post_id RETURN posts.postid%type AS
        v_random_postid int;
    BEGIN
        SELECT postid into v_random_postid
        FROM (
            SELECT postid
            FROM posts
            ORDER BY DBMS_RANDOM.RANDOM)
        WHERE rownum = 1;
        return v_random_postid;
    END;
    
    PROCEDURE populate AS
        v_number_of_comments int;
        v_user_id int;
        v_post_id int;
        v_comment VARCHAR2(512);
    BEGIN
        fill_adjective_list();
        v_number_of_comments := 1000;
        FOR i in 1..v_number_of_comments LOOP
            v_user_id := get_random_user_id();
            v_post_id := get_random_post_id();
            v_comment := create_comment_text();
            INSERT INTO comments (commentid, userid, postid, text) values (i, v_user_id, v_post_id, v_comment);
        END LOOP;
    END;
END populare_comentarii;
/

BEGIN
    populare_comentarii.populate();
    DBMS_OUTPUT.PUT_LINE('random user_id: ' || populare_comentarii.get_random_user_id());
    DBMS_OUTPUT.PUT_LINE('random post_id: ' || populare_comentarii.get_random_post_id());
    DBMS_OUTPUT.PUT_LINE('random comment: ' || populare_comentarii.create_comment_text());
END;