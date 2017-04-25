drop table users_tags;
drop table posts_tags;
drop table posts_resources;

drop table users;
drop table posts;
drop table tags;
drop table resources;
drop table comments;

create table USERS (
  userId        Integer       PRIMARY KEY,
  firstName     varchar2(64)  not null,
  lastName      varchar2(64)  not null,
  email         varchar2(128) not null,
  passwordHash  varchar2(32)  not null,
  isActivated   number(1)     not null,
  role          char          not null,
  address       varchar2(128),
  phone         varchar2(32),
  
  CONSTRAINT email_unique UNIQUE (email)
);

create table POSTS (
  postId        Integer        PRIMARY KEY,
  userId        Integer        not null,
  title         varchar2(128)  not null,
  body          varchar2(4000) not null,
  
  FOREIGN KEY (userId) REFERENCES Users(userId)
);

create table TAGS (
  tagId         Integer       PRIMARY KEY,
  name          Varchar2(128) not null
);

create table RESOURCES (
  resourceId    Integer         PRIMARY KEY,
  name          Varchar2(128)   not null,
  URI           Varchar2(1024)  not null
);

create table COMMENTS (
  commentId     Integer         PRIMARY KEY,
  userId        Integer         not null,
  postId        Integer         not null,
  text          Varchar2(512)   not null,
  
  FOREIGN KEY (userId) REFERENCES Users(userId),
  FOREIGN KEY (postId) REFERENCES Posts(postId)
);

create table USERS_TAGS (
  userId   Integer not null,
  tagId    Integer not null,
  
  FOREIGN KEY (userId) REFERENCES Users(userId),
  FOREIGN KEY (tagId) REFERENCES Tags(tagId)
);

create table POSTS_TAGS (
  postId   Integer not null,
  tagId    Integer not null,
  
  FOREIGN KEY (postId) REFERENCES Posts(postId),
  FOREIGN KEY (tagId) REFERENCES Tags(tagId)
);

create table POSTS_RESOURCES (
  postId      Integer not null,
  resourceId  Integer not null,
  
  FOREIGN KEY (postId) REFERENCES Posts(postId),
  FOREIGN KEY (resourceId) REFERENCES Resources(resourceId)
);