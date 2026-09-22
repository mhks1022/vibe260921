"use server";

import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import * as store from "@/lib/posts";
import { CATEGORIES } from "@/lib/categories";

function sanitizeCategory(value: FormDataEntryValue | null): string {
  const str = (value ?? "").toString().trim();
  return (CATEGORIES as readonly string[]).includes(str) ? str : "자유";
}

export async function createPostAction(formData: FormData) {
  const title = (formData.get("title") ?? "").toString().trim();
  const author = (formData.get("author") ?? "").toString().trim() || "익명";
  const content = (formData.get("content") ?? "").toString().trim();
  const category = sanitizeCategory(formData.get("category"));

  if (!title || !content) {
    throw new Error("제목과 내용을 입력해주세요.");
  }

  const post = await store.createPost({ title, author, content, category });
  revalidatePath("/");
  redirect(`/posts/${post.id}`);
}

export async function updatePostAction(id: string, formData: FormData) {
  const title = (formData.get("title") ?? "").toString().trim();
  const author = (formData.get("author") ?? "").toString().trim() || "익명";
  const content = (formData.get("content") ?? "").toString().trim();
  const category = sanitizeCategory(formData.get("category"));

  if (!title || !content) {
    throw new Error("제목과 내용을 입력해주세요.");
  }

  await store.updatePost(id, { title, author, content, category });
  revalidatePath("/");
  revalidatePath(`/posts/${id}`);
  redirect(`/posts/${id}`);
}

export async function deletePostAction(id: string) {
  await store.deletePost(id);
  revalidatePath("/");
  redirect("/");
}

export async function addCommentAction(postId: string, formData: FormData) {
  const author = (formData.get("author") ?? "").toString().trim() || "익명";
  const content = (formData.get("content") ?? "").toString().trim();

  if (!content) {
    throw new Error("댓글 내용을 입력해주세요.");
  }

  await store.addComment(postId, { author, content });
  revalidatePath(`/posts/${postId}`);
}

export async function deleteCommentAction(postId: string, commentId: string) {
  await store.deleteComment(postId, commentId);
  revalidatePath(`/posts/${postId}`);
}
