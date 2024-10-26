"use client";
import { Card, CardMedia, CardSize, CardTitle } from "@chatui/core";
import { ReactNode } from "react";

interface IChatUICardProps {
  title: string;
  text: string;
  imageUrl?: string;
  cardActions: ReactNode;
  size?: CardSize;
}

export default function ChatUICard(props: IChatUICardProps) {
  const {
    title,
    text,
    imageUrl = "//gw.alicdn.com/tfs/TB1Xv5_vlr0gK0jSZFnXXbRRXXa-427-240.png",
    cardActions,
    size,
  } = props;

  return (
    <Card size={size}>
      {imageUrl && <CardMedia image={imageUrl} />}
      <CardTitle title={title} />
      <span>{text}</span>
      <div className="flex gap-4">{cardActions}</div>
    </Card>
  );
}
