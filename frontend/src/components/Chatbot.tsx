import { useRef, useState } from "react";
import useAutosizeTextArea from "./ui/useAutosizeTextArea";
import { SendHorizonal } from "lucide-react";

interface ChildComponentProps {
  classNameProp: string;
}

function Chatbot({ classNameProp }: ChildComponentProps) {
  const [value, setValue] = useState<string>("");
  const [message, setMessage] = useState<string[]>([]);
  const textAreaRef = useRef<HTMLTextAreaElement>(null);

  useAutosizeTextArea(textAreaRef.current, value);

  const handleChange = (evt: React.ChangeEvent<HTMLTextAreaElement>) => {
    const val = evt.target?.value;
    setValue(val);
  };

  const handleButtonClick = () => {
    // Display the alert with the textarea input value
    setMessage([...message, value]);
    setValue("");
  };

  return (
    <>
      <div className="h-full p-2 flex flex-col gap-2">
        {message.map((e) => {
          return <div className="break-words rounded-md bg-white p-2">{e}</div>;
        })}
      </div>
      <div className={classNameProp}>
        <div className="max-h-[150px] bg-white flex rounded-md items-center px-3">
          <textarea
            id="prompt-text"
            className="max-h-[150px] bg-white rounded-md hover:border-gray-200 focus:border-gray-200 focus:outline-none placeholder:text-gray-400 w-full bg-transparent border-b border-gray-300 text-sm leading-6 py-2 pr-3 resize-none outline-none transition duration-150 ease-in-out"
            onChange={handleChange}
            placeholder="Enter Prompt"
            onKeyDown={(e) => {e.key == 'enter'}}
            ref={textAreaRef}
            rows={1}
            value={value}
          />
          <button
            type="button"
            className="mt-auto mb-1 rounded-full bg-indigo-600 p-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            onClick={handleButtonClick}
          >
            <SendHorizonal size={16} />
          </button>
        </div>
      </div>
    </>
  );
}

export default Chatbot;
