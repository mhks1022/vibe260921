"use client";

import { useRef } from "react";
import { Trash2 } from "lucide-react";
import type { Comment } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function CommentSection({
  comments,
  addComment,
  deleteComment,
}: {
  comments: Comment[];
  addComment: (formData: FormData) => Promise<void>;
  deleteComment: (commentId: string) => Promise<void>;
}) {
  const formRef = useRef<HTMLFormElement>(null);

  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-lg font-semibold">댓글 {comments.length}개</h2>

      {comments.length > 0 && (
        <ul className="flex flex-col gap-3">
          {comments.map((comment) => (
            <li
              key={comment.id}
              className="flex items-start justify-between gap-3 rounded-lg border p-3"
            >
              <div className="flex flex-col gap-1">
                <div className="flex items-center gap-2 text-sm">
                  <span className="font-medium">{comment.author}</span>
                  <span className="text-xs text-muted-foreground">
                    {formatDateTime(comment.createdAt)}
                  </span>
                </div>
                <p className="whitespace-pre-wrap text-sm">
                  {comment.content}
                </p>
              </div>
              <form action={() => deleteComment(comment.id)}>
                <Button
                  type="submit"
                  variant="ghost"
                  size="icon-sm"
                  aria-label="댓글 삭제"
                >
                  <Trash2 className="size-3.5" />
                </Button>
              </form>
            </li>
          ))}
        </ul>
      )}

      <form
        ref={formRef}
        action={async (formData) => {
          await addComment(formData);
          formRef.current?.reset();
        }}
        className="flex flex-col gap-2 rounded-lg border p-3"
      >
        <div className="flex gap-2">
          <Input
            name="author"
            placeholder="작성자"
            maxLength={20}
            className="max-w-40"
          />
        </div>
        <Textarea name="content" placeholder="댓글을 입력하세요" rows={3} required />
        <div className="flex justify-end">
          <Button type="submit" size="sm">
            댓글 등록
          </Button>
        </div>
      </form>
    </div>
  );
}
