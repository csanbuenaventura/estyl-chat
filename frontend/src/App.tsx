"use client";

import { useEffect, useRef, useState } from "react";
import "./chatui-theme.scss";

import Chat, {
  Avatar,
  Bubble,
  MessageProps,
  QuickReplyItemProps,
  useMessages,
} from "@chatui/core";

import { ComposerHandle } from "@chatui/core/lib/components/Composer";

import { ChatAPI } from "@/apis/ChatAPI";
import { FaChevronRight } from "react-icons/fa6";

const initialMessages: MessageProps[] | any[] = [
  {
    _id: "1",
    type: "text",
    content: {
      text: "👋 Hello! I'm ESTYL AI! How can I help you?",
    },
  },
];

const defaultQuickReplies: QuickReplyItemProps[] = [
  {
    icon: "",
    name: "What's the ESTYL AI?",
    isHighlight: true,
    isNew: true,
  },
  {
    name: "How to use it?",
    isHighlight: true,
  },
  {
    name: "What to wear?",
    isHighlight: true,
  },
];

export default function App() {
  // Hooks
  const { messages, appendMsg, setTyping } = useMessages(initialMessages);

  // States
  const [sessionId, setSessionId] = useState<any>(null);
  const [inputText, setInputText] = useState("");
  const [waiting, setWaiting] = useState(false);

  // Composer bileşeni için useRef kullanarak bir referans
  const composerRef = useRef<ComposerHandle>();

  // Functions
  const handleSend = (type: MessageProps["type"], val: any) => {
    // cevap bekleniyorsa buton pasif hale getir
    composerRef.current?.setText("");

    if (type === "text" && val.trim()) {
      const dto = JSON.stringify({
        text: val,
        sessionId: sessionId,
      });

      appendMsg({
        type: "text",
        content: { text: val },
        position: "right",
      });

      setInputText("");
      setWaiting(true);
      setTyping(true);

      ChatAPI.sendMessage(dto)
        .then((response: any) => {
          appendMsg({
            type: "text",
            content: {
              text: response.data.text,
            },
            position: "left",
          });
        })
        .catch((error: any) => {
          console.log(error);
        })
        .finally(() => {
          setWaiting(false);

          setTyping(false);
        });
    }
  };

  const renderMessageContent = (msg: MessageProps) => {
    const { content } = msg;

    // Mesajın sol tarafında her zaman avatarın gösterilmesi için güncelleme
    const showAvatar = msg.position === "left";

    // Mesajın tarihini ve gönderici adını formatlama
    const timeString = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
    let senderName = "";

    if (showAvatar) {
      senderName = "ESTYL AI";
    } else {
      senderName = "Human";
    }

    const messageEl = <>{content.text}</>;

    return (
      <div
        className={`message-container flex ${
          msg.position === "right"
            ? "flex-row-reverse gap-2 items-end"
            : "flex-row gap-2 items-end"
        }`}
      >
        {showAvatar && <Avatar src="/icon.png" />}
        <div
          className={`bubble-container flex flex-col ${
            msg.position === "right" ? "items-end" : "items-start"
          }`}
        >
          <Bubble>{messageEl}</Bubble>
          <div className="mt-2 text-xs text-gray-500">
            {senderName} • {timeString}
          </div>
        </div>
      </div>
    );
  };

  const handleQuickReplyClick = (item: any) => {
    handleSend("text", item.name);
  };

  useEffect(() => {
    setSessionId(Math.floor(Math.random() * 1000000001).toString());
  }, []);

  useEffect(() => {
    const navbarEl = document.querySelector(".Navbar") as HTMLDivElement;
    const chatFooter = document.querySelector(".ChatFooter") as HTMLDivElement;
    const composer = document.querySelector(".Composer") as HTMLDivElement;

    if (navbarEl) {
      // Navbar componentini içerideki chat componentine ekliyoruz

      navbarEl.innerHTML = `
      <div class="Navbar__left">
        <div class="Navbar__image">
          <img src="/icon.png"  alt="ESTYL AI" />
        </div>
        <div class="Navbar__title">ESTYL AI</div>
      </div>
      <div class="Navbar__right">
      </div>
      `;
    }

    if (composer) {
      composer.append(document.querySelector(".chatui-send-btn") as Node);
    }

    if (chatFooter && !document.querySelector(".orbina-footer")) {
      const orbinaFooter = document.createElement("a") as HTMLAnchorElement;
      orbinaFooter.className = "orbina-footer";
      orbinaFooter.href = "https://estyl.ai";
      orbinaFooter.target = "_blank";
      chatFooter.append(orbinaFooter);

      orbinaFooter.innerHTML = `
      <div class="orbina-footer__left">
      <div class="orbina-footer__title">Powered by</div>
    </div>
      <div class="orbina-footer__right">
        <img src="./icon.png" alt="footer" />
        <span>ESTYL AI</span>
      </div>
      <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="0" height="0" class="sprite-symbols">
		<symbol id="icon-chevron-left" viewBox="0 0 20 20">
			<path d="M12.452 4.516c.446.436.481 1.043 0 1.576L8.705 10l3.747 3.908c.481.533.446 1.141 0 1.574-.445.436-1.197.408-1.615 0-.418-.406-4.502-4.695-4.502-4.695a1.095 1.095 0 0 1 0-1.576s4.084-4.287 4.502-4.695c.418-.409 1.17-.436 1.615 0z"></path>
		</symbol>
	
		<symbol id="icon-chevron-right" viewBox="0 0 20 20">
			<path d="M9.163 4.516c.418.408 4.502 4.695 4.502 4.695a1.095 1.095 0 0 1 0 1.576s-4.084 4.289-4.502 4.695c-.418.408-1.17.436-1.615 0-.446-.434-.481-1.041 0-1.574L11.295 10 7.548 6.092c-.481-.533-.446-1.141 0-1.576.445-.436 1.197-.409 1.615 0z"></path>
		</symbol>
    </svg>
      `;
    }
  }, []);

  return (
    <>
      <Chat
        locale="en-US"
        navbar={{
          title: "",
        }}
        messages={messages}
        onInputChange={(e) => setInputText(e)}
        inputOptions={{
          value: inputText,
          onChange: (e: any) => {
            console.log(e);
            return setInputText(e.target.value);
          },
        }}
        renderMessageContent={renderMessageContent}
        quickReplies={defaultQuickReplies}
        onQuickReplyClick={waiting ? () => {} : handleQuickReplyClick}
        onSend={waiting ? () => {} : handleSend}
        placeholder="Type your messages..."
        // @ts-ignore
        composerRef={composerRef}
      />
      {
        <button
          className="chatui-send-btn Composer-sendBtn"
          onClick={
            waiting
              ? () => {}
              : () => {
                  // ChatUI input alanından metni al
                  const textarea = document.querySelector(
                    ".Composer-input"
                  ) as HTMLTextAreaElement;
                  const messageText = textarea.value;
                  // handleSend fonksiyonunu çağır
                  if (messageText.trim()) {
                    handleSend("text", messageText);
                  }
                }
          }
        >
          <FaChevronRight size={16} />
        </button>
      }
    </>
  );
}
