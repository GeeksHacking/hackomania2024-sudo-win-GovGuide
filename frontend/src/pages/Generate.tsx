import Prompt from "../components/Prompt";
import { Toaster } from "@/components/ui/sonner"

function Generate() {
  return (
    <div id="body" className="min-h-[calc(100dvh-28px-80px)] flex items-center">
      <div className="h-full flex flex-col p-3 mx-auto md:justify-center">
        <Prompt />
      </div>
      <Toaster />
    </div>
  );
}

export default Generate;