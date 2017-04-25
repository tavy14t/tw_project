---Returneaza un string cu numere urmate de o virgula
create or replace function string_from_numbers(v_list in number_list) return varchar2 as
  v_str varchar2(1024) := '';
begin
  for i in 1..v_list.count loop
    v_str := v_str || v_list(i) || ',';
  end loop;
  return v_str;
end string_from_numbers;