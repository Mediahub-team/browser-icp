import { useState } from "react";
import Landing1440Light from "../imports/Landing1440Light/index";
import { WaitlistModal } from "./components/WaitlistModal";
import { pickVariant } from "./variants";

export default function App() {
  const [modalOpen, setModalOpen] = useState(false);
  const variant = pickVariant(typeof window !== "undefined" ? window.location.search : "");

  return (
    <div className="size-full">
      <Landing1440Light variant={variant} onCtaClick={() => setModalOpen(true)} />
      {modalOpen && <WaitlistModal variant={variant} onClose={() => setModalOpen(false)} />}
    </div>
  );
}
