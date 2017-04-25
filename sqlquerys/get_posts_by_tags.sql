create or replace function get_posts_by_tags(v_tag_list_string IN VARCHAR2) return varchar2 as
  v_tag_list number_list := numbers_from_string(v_tag_list_string);
  v_nr_found number;
  v_post_ids number_list := number_list();
begin
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
  return string_from_numbers(v_post_ids);
end get_posts_by_tags;