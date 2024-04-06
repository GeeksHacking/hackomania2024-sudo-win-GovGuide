import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";

interface TypewriterMarkdownProps {
  markdownText: string;
}

const TypewriterMarkdown: React.FC<TypewriterMarkdownProps> = ({
  markdownText,
}) => {
  const [displayedText, setDisplayedText] = useState<string>(
    markdownText[0] || ""
  );

  useEffect(() => {
    setDisplayedText(markdownText[0] || "");
    let index = 0;

    const intervalId = setInterval(() => {
      setDisplayedText((prevText) => prevText + markdownText[index]);
      index++;

      if (index === markdownText.length - 1) {
        clearInterval(intervalId);
      }
    }, 15); // Adjust the interval as needed

    return () => clearInterval(intervalId);
  }, [markdownText]);

  return (
    <ReactMarkdown
      className="mt-4 text-sm text-gray-500 break-all flex flex-col gap-1"
    >
      {displayedText}
    </ReactMarkdown>
  );
};

export default TypewriterMarkdown;
