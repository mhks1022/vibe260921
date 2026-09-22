import Link from "next/link";
import { notFound } from "next/navigation";
import { Eye, Pencil } from "lucide-react";
import { getPost, incrementViews } from "@/lib/posts";
import { deletePostAction, addCommentAction, deleteCommentAction } from "@/lib/actions";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { DeletePostButton } from "@/components/board/delete-post-button";
import { CommentSection } from "@/components/board/comment-section";

function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default async function PostDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const post = await getPost(id);

  if (!post) {
    notFound();
  }

  await incrementViews(id);

  const deleteAction = deletePostAction.bind(null, id);
  const addComment = addCommentAction.bind(null, id);
  const deleteComment = deleteCommentAction.bind(null, id);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-3 border-b pb-5">
        <div className="flex items-center gap-2">
          <Badge variant="outline">{post.category}</Badge>
        </div>
        <h1 className="text-2xl font-bold break-words">{post.title}</h1>
        <div className="flex flex-wrap items-center justify-between gap-2 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <span className="font-medium text-foreground">{post.author}</span>
            <span>&middot;</span>
            <span>{formatDateTime(post.createdAt)}</span>
          </div>
          <span className="flex items-center gap-1">
            <Eye className="size-3.5" />
            조회 {post.views}
          </span>
        </div>
      </div>

      <p className="min-h-24 whitespace-pre-wrap leading-relaxed">
        {post.content}
      </p>

      <div className="flex justify-end gap-2">
        <Button
          variant="outline"
          size="sm"
          nativeButton={false}
          render={<Link href={`/posts/${post.id}/edit`} />}
        >
          <Pencil className="size-4" />
          수정
        </Button>
        <DeletePostButton deleteAction={deleteAction} />
      </div>

      <Separator />

      <CommentSection
        comments={post.comments}
        addComment={addComment}
        deleteComment={deleteComment}
      />

      <div>
        <Button variant="secondary" nativeButton={false} render={<Link href="/" />}>
          목록으로
        </Button>
      </div>
    </div>
  );
}
