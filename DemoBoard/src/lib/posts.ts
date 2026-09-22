import { supabase } from "@/lib/supabase";
import type { Comment, Post, PostSummary } from "@/lib/types";

type PostRow = {
  id: string;
  title: string;
  author: string;
  category: string;
  content: string;
  views: number;
  created_at: string;
  updated_at: string;
};

type CommentRow = {
  id: string;
  author: string;
  content: string;
  created_at: string;
};

function toComment(row: CommentRow): Comment {
  return {
    id: row.id,
    author: row.author,
    content: row.content,
    createdAt: row.created_at,
  };
}

function toPost(row: PostRow, comments: CommentRow[]): Post {
  return {
    id: row.id,
    title: row.title,
    author: row.author,
    category: row.category,
    content: row.content,
    views: row.views,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
    comments: comments.map(toComment),
  };
}

function toSummary(row: PostRow, commentCount: number): PostSummary {
  return {
    id: row.id,
    title: row.title,
    author: row.author,
    category: row.category,
    views: row.views,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
    commentCount,
  };
}

export type SortOrder = "latest" | "views";

export async function getPostSummaries(options?: {
  query?: string;
  sort?: SortOrder;
}): Promise<PostSummary[]> {
  const query = options?.query?.trim();

  let request = supabase.from("posts").select("*, comments(count)");

  if (query) {
    const escaped = query.replace(/[%_]/g, (m) => `\\${m}`);
    request = request.or(
      `title.ilike.%${escaped}%,content.ilike.%${escaped}%,author.ilike.%${escaped}%`
    );
  }

  request =
    options?.sort === "views"
      ? request.order("views", { ascending: false })
      : request.order("created_at", { ascending: false });

  const { data, error } = await request;
  if (error) throw error;

  return (
    data as unknown as (PostRow & { comments: { count: number }[] })[]
  ).map((row) => toSummary(row, row.comments[0]?.count ?? 0));
}

export async function getPost(id: string): Promise<Post | undefined> {
  const { data, error } = await supabase
    .from("posts")
    .select("*, comments(*)")
    .eq("id", id)
    .order("created_at", { foreignTable: "comments", ascending: true })
    .maybeSingle();

  if (error) throw error;
  if (!data) return undefined;

  const { comments, ...post } = data as PostRow & { comments: CommentRow[] };
  return toPost(post, comments);
}

export async function incrementViews(id: string): Promise<void> {
  const { error } = await supabase.rpc("increment_post_views", {
    post_id: id,
  });
  if (error) throw error;
}

export async function createPost(input: {
  title: string;
  author: string;
  content: string;
  category: string;
}): Promise<Post> {
  const { data, error } = await supabase
    .from("posts")
    .insert({
      title: input.title,
      author: input.author,
      content: input.content,
      category: input.category,
    })
    .select()
    .single();

  if (error) throw error;
  return toPost(data as PostRow, []);
}

export async function updatePost(
  id: string,
  input: { title: string; author: string; content: string; category: string }
): Promise<Post | undefined> {
  const { data, error } = await supabase
    .from("posts")
    .update({
      title: input.title,
      author: input.author,
      content: input.content,
      category: input.category,
      updated_at: new Date().toISOString(),
    })
    .eq("id", id)
    .select("*, comments(*)")
    .maybeSingle();

  if (error) throw error;
  if (!data) return undefined;

  const { comments, ...post } = data as PostRow & { comments: CommentRow[] };
  return toPost(post, comments);
}

export async function deletePost(id: string): Promise<void> {
  const { error } = await supabase.from("posts").delete().eq("id", id);
  if (error) throw error;
}

export async function addComment(
  postId: string,
  input: { author: string; content: string }
): Promise<Comment | undefined> {
  const { data, error } = await supabase
    .from("comments")
    .insert({
      post_id: postId,
      author: input.author,
      content: input.content,
    })
    .select()
    .single();

  if (error) throw error;
  return toComment(data as CommentRow);
}

export async function deleteComment(
  postId: string,
  commentId: string
): Promise<void> {
  const { error } = await supabase
    .from("comments")
    .delete()
    .eq("id", commentId)
    .eq("post_id", postId);
  if (error) throw error;
}
