import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "SafarGate — Application-readiness copilot" },
      {
        name: "description",
        content:
          "SafarGate helps applicants confirm program eligibility from their own documents, privately and on their terms.",
      },
      { property: "og:title", content: "SafarGate — Application-readiness copilot" },
      {
        property: "og:description",
        content:
          "Confirm eligibility from your own documents. Nothing is sent, stored, or used for training.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

function Index() {
  return (
    <iframe
      src="/safargate.html"
      title="SafarGate"
      style={{
        position: "fixed",
        inset: 0,
        width: "100%",
        height: "100%",
        border: "none",
      }}
    />
  );
}
