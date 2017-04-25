create or replace function get_unused_id(table_name IN VARCHAR2) return number as
  v_max number;
  v_exst number;
begin
  if lower(table_name) = 'users' then
    select max(userid) into v_max from users;
    for i in 1..v_max loop
      select case when exists(select * from users where userid = i) 
        then 1 else 0 end into v_exst from dual;
      if v_exst = 0 then
        return i;
      end if;
    end loop;
    return v_max + 1;
  elsif lower(table_name) = 'posts' then
    select max(postid) into v_max from posts;
    for i in 1..v_max loop
      select case when exists(select * from posts where postid = i) 
        then 1 else 0 end into v_exst from dual;
      if v_exst = 0 then
        return i;
      end if;
    end loop;
    return v_max + 1;
  elsif lower(table_name) = 'comments' then
    select max(commentid) into v_max from comments;
    for i in 1..v_max loop
      select case when exists(select * from comments where commentid = i) 
        then 1 else 0 end into v_exst from dual;
      if v_exst = 0 then
        return i;
      end if;
    end loop;
    return v_max + 1;
  elsif lower(table_name) = 'resources' then
    select max(resourceid) into v_max from resources;
    for i in 1..v_max loop
      select case when exists(select * from resources where resourceid = i) 
        then 1 else 0 end into v_exst from dual;
      if v_exst = 0 then
        return i;
      end if;
    end loop;
    return v_max + 1;
  elsif lower(table_name) = 'tags' then
    select max(tagid) into v_max from tags;
    for i in 1..v_max loop
      select case when exists(select * from tags where tagid = i) 
        then 1 else 0 end into v_exst from dual;
      if v_exst = 0 then
        return i;
      end if;
    end loop;
    return v_max + 1;
  end if;
end get_unused_id;