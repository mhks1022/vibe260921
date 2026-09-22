import { createPostAction } from "@/lib/actions";
import { CATEGORIES } from "@/lib/categories";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export default function WritePage() {
  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl font-bold">글쓰기</h1>

      <form action={createPostAction} className="flex flex-col gap-5">
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="flex flex-col gap-2">
            <Label htmlFor="author">작성자</Label>
            <Input id="author" name="author" placeholder="익명" maxLength={20} />
          </div>
          <div className="flex flex-col gap-2">
            <Label htmlFor="category">카테고리</Label>
            <Select name="category" defaultValue={CATEGORIES[0]}>
              <SelectTrigger id="category" className="w-full">
                <SelectValue placeholder="카테고리 선택" />
              </SelectTrigger>
              <SelectContent>
                {CATEGORIES.map((category) => (
                  <SelectItem key={category} value={category}>
                    {category}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="flex flex-col gap-2">
          <Label htmlFor="title">제목</Label>
          <Input
            id="title"
            name="title"
            placeholder="제목을 입력하세요"
            required
            maxLength={100}
          />
        </div>

        <div className="flex flex-col gap-2">
          <Label htmlFor="content">내용</Label>
          <Textarea
            id="content"
            name="content"
            placeholder="내용을 입력하세요"
            required
            rows={12}
          />
        </div>

        <div className="flex justify-end gap-2">
          <Button type="submit">등록</Button>
        </div>
      </form>
    </div>
  );
}
