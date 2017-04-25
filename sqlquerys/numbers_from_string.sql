---Trebuie sa nu contina spatii si fiecare numar sa fie urmat de o virgula
create or replace function numbers_from_string(v_str IN VARCHAR2) return number_list as
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
