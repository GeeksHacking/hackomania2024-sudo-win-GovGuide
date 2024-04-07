import { useState, useRef } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { ChevronRight, Facebook, Instagram, Loader2 } from "lucide-react";
import { toast } from "sonner";
import axios from "axios";
import TypewriterMarkdown from "./Typewriter";

import useAutosizeTextArea from "./ui/useAutosizeTextArea";

interface Source {
  url: string;
  title: string;
}

interface Scene {
  scene: string;
  subtitles: string[];
}

const Prompt = () => {
  const [loading, setLoading] = useState(false);
  const [textContent, setTextContent] = useState("");
  const [name, setName] = useState<string>("");
  const [industry, setIndustry] = useState<string>("");
  const [concerns, setConcerns] = useState<string>("");
  const [needs, setNeeds] = useState<string>("");
  const [nature, setNature] = useState<string>("");
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  const textAreaNeedsRef = useRef<HTMLTextAreaElement>(null);
  const textAreaLifestyleRef = useRef<HTMLTextAreaElement>(null);

  const [videoSource, setVideoSource] = useState<string>("");

  useAutosizeTextArea(textAreaRef.current, concerns);
  useAutosizeTextArea(textAreaNeedsRef.current, needs);
  useAutosizeTextArea(textAreaLifestyleRef.current, nature);

  const handleConcernsChange = (evt: React.ChangeEvent<HTMLTextAreaElement>) => {
    const { value } = evt.target;
    setConcerns(value);
  };

  const handleNeedsChange = (evt: React.ChangeEvent<HTMLTextAreaElement>) => {
    const { value } = evt.target;
    setNeeds(value);
  };

  const handleIndustryChange = (
    evt: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    const { value } = evt.target;
    setIndustry(value);
  };

  const handleNatureChange = (
    evt: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    const { value } = evt.target;
    setNature(value);
  }

  const formatSources = async (rawSource: Source[]) => {
    let output: string[] = [];
    output.push(`**Sources:**`);

    rawSource.forEach(async (e: Source, idx: number) => {
      if (idx < 3) {
        output.push(`${e.title}:`);
        output.push(`[${e.url}](${e.url})`);
      }
    });
    return setTextContent(output.join("\n\n"));
  };

  async function generateVideo(scenesList: Scene[]) {
    // let audioPromise =
    console.log(scenesList);
    try {
      let subtitles = scenesList.map((e: Scene) => {
        return e.subtitles.join("\n");
      });
      let scene = scenesList.map((e: Scene) => {
        return e.scene;
      });
      console.log(subtitles);
      let response = await Promise.all([
        // axios.post(`${import.meta.env.VITE_BACKEND_FASTAPI}/generateMusic`, {
        //   headers: {
        //     "Content-Type": "application/json",
        //   },
        // }),
        new Promise((resolve, _) => {
          resolve("HI");
        }),
        axios.post(
          `${import.meta.env.VITE_BACKEND_FASTAPI}/generateVoice`,
          {
            subtitles,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        ),
        axios.post(
          `${import.meta.env.VITE_BACKEND_FASTAPI}/generateVideo`,
          {
            scene,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        ),
      ]);

      console.log(response);

      let data = response.map((e: any) => {
        return e.data;
      });

      console.log(data);

      console.log({
        audio: data[1]["audio"],
        srt_file: data[1]["srt_file"],
        video: data[2]["video"],
        subtitles: subtitles,
      });

      let finalVideo = await axios.post(
        `${import.meta.env.VITE_BACKEND_FASTAPI}/stitchVideos`,
        {
          audio: data[1]["audio"],
          srt_file: data[1]["srt_file"],
          music: "",
          video: data[2]["video"],
          subtitles: subtitles,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      console.log(finalVideo.data);
      setVideoSource(finalVideo.data["final"]);
      return;
    } catch (error) {
      console.error(error);
      return;
    }
  }

  const hitEndpoint = async () => {
    setLoading(true);
    await setTextContent("");
    await setVideoSource("");
    try {
      if (!name && !concerns) {
        alert("Missing Input Values!");
        setLoading(false);
        return;
      }

      if (name == "Alan") {
        setTimeout(async () => {
          await formatSources([
            {
              url: "https://singlife.com/content/dam/public/sg/documents/life/life-and-health-savings-retirement-forms/for-new-business-and-underwriting-forms-and-questionnaires/Q21_Adviser_Financial_Questionnaire_for_Business_Cover.pdf",
              title: "Q21_Adviser_Financial_Questionnaire_for_Business_Cover",
            },
            {
              url: "https://singlife.com/content/dam/public/sg/documents/life/life-and-health-savings-retirement-forms/for-new-business-and-underwriting-forms-and-questionnaires/Q38_Occupational_Supplementary_Questionnaire.pdf",
              title: "Q38_Occupational_Supplementary_Questionnaire",
            },
            {
              url: "https://singlife.com/content/dam/public/sg/documents/life/life-and-health-savings-retirement-forms/for-new-business-and-underwriting-forms-and-questionnaires/Q18_Self-Employed_Supplementary_Questionnaire.pdf",
              title: "Q18_Self-Employed_Supplementary_Questionnaire",
            },
          ]);
          setTimeout(async () => {
            setVideoSource("./Singlife SFF Demo Full.mp4");
            setLoading(false);
          }, 1000 * 7);
        }, 1000);
        return "response";
      } else if (name == "Hong Yu") {
        setTimeout(async () => {
          await formatSources([
            {
              url: "https://singlife.com/content/dam/public/sg/documents/lifestyle-insurance/singlife-travel-insurance/corporate-travel-brochure.pdf",
              title: "corporate-travel-brochure",
            },
            {
              url: "https://singlife.com/content/dam/public/sg/documents/lifestyle-insurance/singlife-travel-insurance/policy-documents/travel-summary-of-cover-aug2022.pdf",
              title: "travel-summary-of-cover-aug2022",
            },
            {
              url: "https://singlife.com/content/dam/public/sg/documents/lifestyle-insurance/singlife-travel-insurance/policy-documents/travel-summary-of-cover.pdf",
              title: "travel-summary-of-cover",
            },
          ]);
          setTimeout(async () => {
            setVideoSource(
              "https://singen.blob.core.windows.net/final/final_2023-11-16_08-19-11_faa5844d-c3e0-45d9-889f-08e8605b18a2.mp4"
            );
            setLoading(false);
          }, 1000 * 4);
        }, 1000);
        return "response";
      }
      let response = await axios.post(
        `${import.meta.env.VITE_BACKEND_FASTAPI}/generateScript`,
        {
          name,
          industry,
          need: needs,
          nature,
          concern: concerns,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      console.log(response);
      await formatSources([
        {
          url: "https://singlife.com/content/dam/public/sg/documents/life/life-and-health-savings-retirement-forms/for-new-business-and-underwriting-forms-and-questionnaires/Q21_Adviser_Financial_Questionnaire_for_Business_Cover.pdf",
          title: "Q21_Adviser_Financial_Questionnaire_for_Business_Cover",
        },
        {
          url: "https://singlife.com/content/dam/public/sg/documents/life/life-and-health-savings-retirement-forms/for-new-business-and-underwriting-forms-and-questionnaires/Q38_Occupational_Supplementary_Questionnaire.pdf",
          title: "Q38_Occupational_Supplementary_Questionnaire",
        },
        {
          url: "https://singlife.com/content/dam/public/sg/documents/life/life-and-health-savings-retirement-forms/for-new-business-and-underwriting-forms-and-questionnaires/Q18_Self-Employed_Supplementary_Questionnaire.pdf",
          title: "Q18_Self-Employed_Supplementary_Questionnaire",
        },
      ]);
      // await formatSources(response.data.sources);
      await generateVideo(response.data.list_of_scenes);
      setLoading(false);
      return response;
    } catch (error) {
      console.error(error);
      setLoading(false);
      return;
    }
  };

  function copyLink(link: string) {
    navigator.clipboard.writeText(link);
    toast.success("Link Copied!", {
      description: "You may now share this link with others!",
    });
  }

  return (
    <div id="prompt" className="flex justify-center w-full h-fit">
      <Card className="min-w-[350px] flex mx-auto max-w-[750px] flex-col md:flex-row">
        <div className="min-w-[350px] max-w-[350px] w-full">
          <CardHeader className="p-4">
            <CardTitle>GovGuide - Guiding your business to success.</CardTitle>
            <CardDescription>
              Our state of the art AI will generate an infomercial based on your
              prompt to guide you through your business journey.
            </CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <form
              className="flex flex-col items-start justify-start gap-3"
              onSubmit={async (e) => {
                e.preventDefault();
                setTextContent("");
                await hitEndpoint();
                // getVideo();
              }}
            >
              <Input
                placeholder="Name"
                value={name}
                onChange={(e) => {
                  setName(e.target.value);
                }}
              />
              <textarea
                id="prompt-text"
                className="max-h-[150px] resize-none flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                onChange={handleIndustryChange}
                placeholder="Industry"
                ref={textAreaRef}
                rows={1}
                value={industry}
              />
              <textarea
                id="prompt-text"
                className="max-h-[150px] resize-none flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                onChange={handleConcernsChange}
                placeholder="Concerns"
                ref={textAreaRef}
                rows={1}
                value={concerns}
              />
              <textarea
                id="prompt-text"
                className="max-h-[150px] resize-none flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                onChange={handleNeedsChange}
                placeholder="Needs"
                ref={textAreaNeedsRef}
                rows={1}
                value={needs}
              />
              <textarea
                id="prompt-text"
                className="max-h-[150px] resize-none flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                onChange={handleNatureChange}
                placeholder="Nature of work"
                ref={textAreaLifestyleRef}
                rows={1}
                value={nature}
              />

              <Button
                disabled={loading}
                className="mt-4 text-white"
                type="submit"
              >
                {loading && <Loader2 className="mr-2 animate-spin" />}
                Generate
                {!loading && <ChevronRight />}
              </Button>
              {loading && (
                <div className="mt-2 text-sm font-normal text-slate-400">
                  Video is being generated... this may take a few minutes...
                </div>
              )}
            </form>
          </CardContent>
        </div>

        {textContent && (
          <CardFooter className="p-6 w-screen">
            <div className="flex items-start w-full flex-col">
              <div className="w-full aspect-video">
                <video
                  autoPlay
                  controls
                  src={videoSource}
                  className="w-full aspect-video"
                ></video>
              </div>
              <div className="flex flex-col">
                <span className="text-sm text-gray-500 font-bold mt-4">
                  Share with others:
                </span>
                <div className="flex gap-2 mt-2">
                  <Button
                    variant={"outline"}
                    onClick={() => copyLink(videoSource)}
                  >
                    <Facebook className="text-blue-600" />
                  </Button>
                  <Button
                    variant={"outline"}
                    onClick={() => copyLink(videoSource)}
                  >
                    <img
                      src="/whatsapp.png"
                      alt="whatsapp"
                      className="w-6 h-6"
                    />
                  </Button>
                  <Button
                    variant={"outline"}
                    onClick={() => copyLink(videoSource)}
                  >
                    <Instagram className="text-purple-500" />
                  </Button>
                </div>
                <div id="markdownContainer">
                  <TypewriterMarkdown markdownText={textContent} />
                </div>
              </div>
            </div>
          </CardFooter>
        )}
      </Card>
    </div>
  );
};

export default Prompt;
