import { useState } from "react";
import imgSuccess from "../../imports/LandingForm/7696dedb881593f0ce1aa6829001696e573de64c.png";
import imgError from "../../imports/LandingForm/56a98f99601189c44980d645a881539764f62a04.png";

type Step = "form" | "success" | "error";
type Tab = "email" | "phone";

interface WaitlistModalProps {
  onClose: () => void;
}

export function WaitlistModal({ onClose }: WaitlistModalProps) {
  const [step, setStep] = useState<Step>("form");
  const [tab, setTab] = useState<Tab>("email");
  const [value, setValue] = useState("");
  const [fieldError, setFieldError] = useState("");
  const [loading, setLoading] = useState(false);

  function validate(): boolean {
    if (tab === "email") {
      const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
      if (!ok) { setFieldError("Email указан неверно"); return false; }
    } else {
      const digits = value.replace(/\D/g, "");
      if (digits.length < 11) { setFieldError("Пожалуйста, введите номер"); return false; }
    }
    setFieldError("");
    return true;
  }

  async function handleSubmit() {
    if (!validate()) return;
    setLoading(true);
    await new Promise(r => setTimeout(r, 800));
    setLoading(false);
    setStep("success");
  }

  function handleRetry() {
    setValue("");
    setFieldError("");
    setStep("form");
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ backgroundColor: "rgba(0,11,33,0.5)" }}
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className="bg-white rounded-[16px] w-full max-w-[327px] px-8 py-10 flex flex-col gap-8 items-center relative">

        {step === "form" && (
          <>
            <button
              onClick={onClose}
              className="absolute top-4 right-4 flex items-center justify-center w-10 h-10 rounded-[24px] bg-white border-0 cursor-pointer"
              aria-label="Закрыть"
            >
              <svg width="24" height="24" fill="none" viewBox="0 0 24 24">
                <path d="M18 6L6 18M6 6l12 12" stroke="#000B21" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>

            <div className="flex flex-col gap-4 items-center text-center w-full">
              <p className="font-['Manrope:Bold',sans-serif] font-bold text-[24px] leading-[30px] text-[#000b21] w-full">Ранний доступ</p>
              <p className="font-['Manrope:Regular',sans-serif] font-normal text-[16px] leading-[24px] text-[#666d7a] w-full">
                Оставьте email или телефон, чтобы получить приглашение и бонус +200 ₽ на первую покупку
              </p>
            </div>

            <div className="flex flex-col gap-4 w-full">
              <div className="flex w-full rounded-[8px] overflow-hidden border border-[#e0dfff]">
                <button
                  onClick={() => { setTab("email"); setValue(""); setFieldError(""); }}
                  className={`flex-1 py-2 text-[16px] leading-[24px] font-['Inter:Semi_Bold',sans-serif] font-semibold border-0 cursor-pointer transition-colors ${tab === "email" ? "bg-[#6461ff] text-white" : "bg-white text-[#999da6]"}`}
                >
                  Email
                </button>
                <button
                  onClick={() => { setTab("phone"); setValue(""); setFieldError(""); }}
                  className={`flex-1 py-2 text-[16px] leading-[24px] font-['Inter:Semi_Bold',sans-serif] font-semibold border-0 cursor-pointer transition-colors ${tab === "phone" ? "bg-[#6461ff] text-white" : "bg-white text-[#999da6]"}`}
                >
                  Телефон
                </button>
              </div>

              <div className="flex flex-col gap-2 w-full">
                <div className={`relative w-full rounded-[8px] border ${fieldError ? "border-[#ff4242]" : "border-[#e0dfff]"}`}>
                  <input
                    type={tab === "email" ? "email" : "tel"}
                    placeholder={tab === "email" ? "Введите email" : "+7 (___) ___-__-__"}
                    value={value}
                    onChange={e => { setValue(e.target.value); setFieldError(""); }}
                    className="w-full px-4 py-4 text-[16px] leading-[24px] font-['Inter:Regular',sans-serif] font-normal text-[#000b21] bg-transparent border-0 outline-none rounded-[8px] placeholder:text-[#999da6]"
                  />
                </div>
                {fieldError && (
                  <p className="font-['Manrope:Regular',sans-serif] font-normal text-[16px] leading-[24px] text-[#ff4242]">{fieldError}</p>
                )}
              </div>
            </div>

            <div className="flex flex-col gap-2 w-full">
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="w-full bg-[#6461ff] rounded-[8px] px-6 py-4 text-[16px] leading-[24px] font-['Inter:Semi_Bold',sans-serif] font-semibold text-white border-0 cursor-pointer disabled:opacity-60"
              >
                {loading ? "Отправка..." : "Записаться"}
              </button>
              <p className="font-['Manrope:Regular',sans-serif] font-normal text-[12px] text-[#999da6] text-center w-full">
                Нажимая на кнопку вы соглашаетесь на обработку данных
              </p>
            </div>
          </>
        )}

        {step === "success" && (
          <>
            <img src={imgSuccess} alt="" className="w-[85px] h-[85px] object-cover" />
            <div className="flex flex-col gap-4 items-center text-center w-full">
              <p className="font-['Manrope:Bold',sans-serif] font-bold text-[24px] leading-[30px] text-[#000b21] w-full">Заявка принята</p>
              <p className="font-['Manrope:Regular',sans-serif] font-normal text-[16px] leading-[24px] text-[#666d7a] w-full">
                Спасибо! Мы добавили вас в список раннего доступа и скоро свяжемся с вами
              </p>
            </div>
            <button
              onClick={onClose}
              className="w-full bg-[#6461ff] rounded-[8px] px-6 py-4 text-[16px] leading-[24px] font-['Inter:Semi_Bold',sans-serif] font-semibold text-white border-0 cursor-pointer"
            >
              Хорошо
            </button>
          </>
        )}

        {step === "error" && (
          <>
            <img src={imgError} alt="" className="w-[85px] h-[85px] object-cover" />
            <div className="flex flex-col gap-4 items-center text-center w-full">
              <p className="font-['Manrope:Bold',sans-serif] font-bold text-[24px] leading-[30px] text-[#000b21] w-full">Не удалось отправить заявку</p>
              <p className="font-['Manrope:Regular',sans-serif] font-normal text-[16px] leading-[24px] text-[#666d7a] w-full">
                Кажется, произошла ошибка. Попробуйте ещё раз
              </p>
            </div>
            <button
              onClick={handleRetry}
              className="w-full bg-[#6461ff] rounded-[8px] px-6 py-4 text-[16px] leading-[24px] font-['Inter:Semi_Bold',sans-serif] font-semibold text-white border-0 cursor-pointer"
            >
              Повторить
            </button>
          </>
        )}
      </div>
    </div>
  );
}
