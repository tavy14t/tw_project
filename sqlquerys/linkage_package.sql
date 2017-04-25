CREATE OR REPLACE PACKAGE BODY LINKAGE
AS

function get_posts_by_tags(v_tag_list_string IN VARCHAR2) return varchar2 as
  v_tag_list number_list;
  v_nr_found number;
  v_post_ids number_list;
  v_result Varchar2(1024);
  ex_no_data EXCEPTION;
begin
  v_tag_list := numbers_from_string(v_tag_list_string);
  v_post_ids := number_list();

  for v_ent in (select postid from posts) loop
    v_nr_found := 0;
    for v_ent2 in (select tagid from posts_tags where postid = v_ent.postid) loop
      for i in 1..v_tag_list.count loop
        if v_ent2.tagid = v_tag_list(i) then
          v_nr_found := v_nr_found + 1;
        end if;
      end loop;
    end loop;
    if v_nr_found = v_tag_list.count then
      v_post_ids.extend();
      v_post_ids(v_post_ids.count) := v_ent.postid;
    end if;
  end loop;

  v_result := string_from_numbers(v_post_ids);
  if v_result is null then
	raise ex_no_data;
  end if;
  return v_result;
  EXCEPTION
    WHEN ex_no_data THEN
        RAISE_APPLICATION_ERROR(-20001,'No data found!');
end get_posts_by_tags;

function string_from_numbers(v_list in number_list) return varchar2 as
  v_str varchar2(1024) := '';
begin
  for i in 1..v_list.count loop
    v_str := v_str || v_list(i) || ',';
  end loop;
  return v_str;
end string_from_numbers;

function numbers_from_string(v_str IN VARCHAR2) return number_list as
  v_found int := 0;
  v_nr number := 0;
  v_list number_list := number_list();
begin
  for i in 1..length(v_str) loop
    if substr(v_str, i, 1) = ',' then
      v_nr := TO_NUMBER(substr(v_str, v_found + 1, i - v_found - 1));
      v_found := i;
      v_list.extend();
      v_list(v_list.count) := v_nr;
    end if;
  end loop;
  return v_list;
end numbers_from_string;

END LINKAGE;
