CREATE OR REPLACE FUNCTION GET_STATS (POST_ID IN VARCHAR2) RETURN VARCHAR2
IS
	v_fname Varchar2(64);
	v_lname Varchar2(64);
	v_mail Varchar2(128);
	v_result Varchar2(1024);
BEGIN
	SELECT firstname, lastname, email
	INTO v_fname, v_lname, v_mail
	FROM users JOIN posts 
	ON users.userid = posts.userid
	AND posts.postid = post_id;
	v_result := 'Author: ' || v_fname || ' ' || v_lname || '#';
	v_result := v_result || 'Contact: ' || v_mail || '#';
	v_result := v_result || 'Post tags:#';
	FOR i IN (	SELECT tags.name 
				FROM tags JOIN posts_tags 
				ON tags.tagid = posts_tags.tagid 
				WHERE posts_tags.postid = post_id)
		LOOP
			v_result := v_result || '    ' || i.name || '#';
		END LOOP;

	v_result := v_result || 'Resources:#';
	FOR i IN (	SELECT resources.name, resources.uri
				FROM resources JOIN posts_resources
				ON resources.resourceid = posts_resources.postid
				WHERE posts_resources.postid = post_id)
		LOOP
			v_result := v_result || '    ' || i.name 
			            || ' - ' || i.uri  || '#';
		END LOOP;
			
	RETURN v_result;
END;
