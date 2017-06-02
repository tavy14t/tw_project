create table USERS (
  userId        Integer        PRIMARY KEY not null,
  firstName     varchar2(255)  not null,
  lastName      varchar2(255)  not null,
  email         varchar2(255)  not null,
  passwordHash  varchar2(255)  not null,
  isActivated   varchar2(255),
  role          varchar2(255),
  address       varchar2(255),
  phone         varchar2(255)
);

create table POSTS (
  postId        Integer        PRIMARY KEY not null,
  userId        Integer        not null,
  title         varchar2(255)  not null,
  body          varchar2(4095) not null
);

create table TAGS (
  tagId         Integer       PRIMARY KEY not null,
  name          Varchar2(255) not null
);

create table RESOURCES (
  resourceId    Integer         PRIMARY KEY not null,
  name          Varchar2(255)   not null,
  URI           Varchar2(255)   not null
);

create table COMMENTS (
  commentId     Integer         PRIMARY KEY not null,
  userId        Integer         not null,
  postId        Integer         not null,
  text          Varchar2(4095)  not null
);

create table USERS_TAGS (
  userId   Integer not null,
  tagId    Integer not null
);

create table POSTS_TAGS (
  postId   Integer not null,
  tagId    Integer not null
);

create table POSTS_RESOURCES (
  postId      Integer not null,
  resourceId  Integer not null
);
