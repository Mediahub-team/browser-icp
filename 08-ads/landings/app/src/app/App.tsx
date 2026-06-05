import { useState } from "react";
import Landing1440Light from "../imports/Landing1440Light/index";
import { WaitlistModal } from "./components/WaitlistModal";

export default function App() {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <div className="size-full">
      <Landing1440Light onCtaClick={() => setModalOpen(true)} />
      {modalOpen && <WaitlistModal onClose={() => setModalOpen(false)} />}
    </div>
  );
}
