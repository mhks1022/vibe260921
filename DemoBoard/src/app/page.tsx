import Link from "next/link";
import { getPostSummaries, type SortOrder } from "@/lib/posts";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { MessageSquare, Eye, PenSquare } from "lucide-react";

function formatDate(iso: string): string {
  const date = new Date(iso);
  return date.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
}

export default async function HomePage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; sort?: string }>;
}) {
  const params = await searchParams;
  const query = params.q ?? "";
  const sort: SortOrder = params.sort === "views" ? "views" : "latest";

  const posts = await getPostSummaries({ query, sort });

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <h1 className="text-2xl font-bold">게시판</h1>
        <p className="text-sm text-muted-foreground">
          총 {posts.length}개의 글이 있습니다.
        </p>
      </div>

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <form className="flex w-full max-w-sm items-center gap-2" action="/">
          {sort !== "latest" && (
            <input type="hidden" name="sort" value={sort} />
          )}
          <Input
            type="text"
            name="q"
            placeholder="제목, 내용, 작성자 검색"
            defaultValue={query}
          />
          <Button type="submit" variant="secondary">
            검색
          </Button>
        </form>

        <div className="flex items-center gap-2">
          <div className="flex overflow-hidden rounded-md border">
            <Link
              href={{ pathname: "/", query: { ...(query ? { q: query } : {}), sort: "latest" } }}
              className={`px-3 py-1.5 text-sm ${
                sort === "latest"
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent"
              }`}
            >
              최신순
            </Link>
            <Link
              href={{ pathname: "/", query: { ...(query ? { q: query } : {}), sort: "views" } }}
              className={`px-3 py-1.5 text-sm ${
                sort === "views"
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent"
              }`}
            >
              조회순
            </Link>
          </div>
          <Button nativeButton={false} render={<Link href="/write" />}>
            <PenSquare className="size-4" />
            글쓰기
          </Button>
        </div>
      </div>

      <Separator />

      {posts.length === 0 ? (
        <div className="flex flex-col items-center justify-center gap-2 py-24 text-center text-muted-foreground">
          <p>{query ? "검색 결과가 없습니다." : "아직 작성된 글이 없습니다."}</p>
          <Button
            variant="outline"
            className="mt-2"
            nativeButton={false}
            render={<Link href="/write" />}
          >
            첫 글 작성하기
          </Button>
        </div>
      ) : (
        <ul className="flex flex-col divide-y rounded-lg border">
          {posts.map((post) => (
            <li key={post.id}>
              <Link
                href={`/posts/${post.id}`}
                className="flex flex-col gap-1.5 px-4 py-3.5 transition-colors hover:bg-accent/50 sm:flex-row sm:items-center sm:justify-between"
              >
                <div className="flex min-w-0 flex-col gap-1">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline">{post.category}</Badge>
                    <span className="truncate font-medium">{post.title}</span>
                    {post.commentCount > 0 && (
                      <span className="text-xs text-muted-foreground">
                        [{post.commentCount}]
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span>{post.author}</span>
                    <span>&middot;</span>
                    <span>{formatDate(post.createdAt)}</span>
                  </div>
                </div>
                <div className="flex shrink-0 items-center gap-3 text-xs text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <Eye className="size-3.5" />
                    {post.views}
                  </span>
                  <span className="flex items-center gap-1">
                    <MessageSquare className="size-3.5" />
                    {post.commentCount}
                  </span>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
