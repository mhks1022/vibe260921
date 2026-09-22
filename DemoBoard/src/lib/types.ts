export type Comment = {
  id: string;
  author: string;
  content: string;
  createdAt: string;
};

export type Post = {
  id: string;
  title: string;
  author: string;
  content: string;
  category: string;
  views: number;
  createdAt: string;
  updatedAt: string;
  comments: Comment[];
};

export type PostSummary = Omit<Post, "content" | "comments"> & {
  commentCount: number;
};
