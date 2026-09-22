-- Run this in the Supabase SQL editor (or via `supabase db push`)
-- to create the tables DemoBoard needs.

create table if not exists posts (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  author text not null,
  category text not null,
  content text not null,
  views integer not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists comments (
  id uuid primary key default gen_random_uuid(),
  post_id uuid not null references posts(id) on delete cascade,
  author text not null,
  content text not null,
  created_at timestamptz not null default now()
);

create index if not exists comments_post_id_idx on comments (post_id);

create or replace function increment_post_views(post_id uuid)
returns void
language sql
as $$
  update posts set views = views + 1 where id = post_id;
$$;

grant execute on function increment_post_views(uuid) to anon;

-- DemoBoard has no auth; the app talks to Supabase with the public
-- "publishable" key, so RLS must explicitly allow anonymous read/write.
alter table posts enable row level security;
alter table comments enable row level security;

create policy "Public read posts" on posts for select using (true);
create policy "Public insert posts" on posts for insert with check (true);
create policy "Public update posts" on posts for update using (true) with check (true);
create policy "Public delete posts" on posts for delete using (true);

create policy "Public read comments" on comments for select using (true);
create policy "Public insert comments" on comments for insert with check (true);
create policy "Public delete comments" on comments for delete using (true);

-- Seed data matching the previous in-memory demo content.
insert into posts (title, author, category, content, views, created_at, updated_at)
values
  (
    'DemoBoard에 오신 것을 환영합니다',
    '관리자',
    '공지',
    'DemoBoard는 Next.js, TypeScript, shadcn/ui로 만든 게시판 데모 사이트입니다.' || chr(10) || chr(10) || '자유롭게 글을 작성하고 댓글을 남겨보세요.',
    12,
    '2026-09-01T09:00:00.000Z',
    '2026-09-01T09:00:00.000Z'
  ),
  (
    'Next.js App Router 사용 후기',
    '개발자김',
    '자유',
    'App Router와 서버 컴포넌트를 함께 써보니 데이터 패칭이 훨씬 단순해졌습니다.' || chr(10) || '서버 액션으로 폼 처리도 간편하네요.',
    34,
    '2026-09-05T04:20:00.000Z',
    '2026-09-05T04:20:00.000Z'
  ),
  (
    'shadcn/ui 컴포넌트 추천 조합',
    '디자이너박',
    '정보',
    'Card + Badge + Separator 조합이 목록형 UI를 만들 때 특히 유용합니다.' || chr(10) || 'Dialog와 AlertDialog는 삭제 확인 같은 곳에 잘 어울려요.',
    21,
    '2026-09-10T13:15:00.000Z',
    '2026-09-10T13:15:00.000Z'
  );

insert into comments (post_id, author, content, created_at)
select id, '방문자', '깔끔한 게시판이네요!', '2026-09-01T10:30:00.000Z'
from posts where title = 'DemoBoard에 오신 것을 환영합니다';

insert into comments (post_id, author, content, created_at)
select id, '방문자', '저도 그 조합 써봐야겠어요', '2026-09-11T02:00:00.000Z'
from posts where title = 'shadcn/ui 컴포넌트 추천 조합';
