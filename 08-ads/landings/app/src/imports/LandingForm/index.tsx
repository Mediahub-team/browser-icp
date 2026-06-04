import svgPaths from "./svg-apwaotjra2";
import imgImage3651 from "./7696dedb881593f0ce1aa6829001696e573de64c.png";
import imgImage3652 from "./56a98f99601189c44980d645a881539764f62a04.png";
type LandingFormProps = {
  className?: string;
  property1?: "Default" | "Variant2" | "Variant3" | "Variant4" | "Variant5" | "Variant6" | "Variant7" | "Variant8" | "Variant9" | "Variant10";
};

export default function LandingForm({ className, property1 = "Default" }: LandingFormProps) {
  const isDefaultOrVariant2OrVariant3OrVariant4OrVariant5OrVariant6Or = ["Default", "Variant2", "Variant3", "Variant4", "Variant5", "Variant6", "Variant7", "Variant8"].includes(property1);
  const isVariant10 = property1 === "Variant10";
  const isVariant3 = property1 === "Variant3";
  const isVariant3OrVariant4 = ["Variant3", "Variant4"].includes(property1);
  const isVariant4 = property1 === "Variant4";
  const isVariant5 = property1 === "Variant5";
  const isVariant5OrVariant6OrVariant7OrVariant8 = ["Variant5", "Variant6", "Variant7", "Variant8"].includes(property1);
  const isVariant6 = property1 === "Variant6";
  const isVariant7 = property1 === "Variant7";
  const isVariant7OrVariant8 = ["Variant7", "Variant8"].includes(property1);
  const isVariant8 = property1 === "Variant8";
  const isVariant9 = property1 === "Variant9";
  const isVariant9OrVariant10 = ["Variant9", "Variant10"].includes(property1);
  return (
    <div className={className || `bg-white content-stretch flex flex-col gap-[32px] items-center px-[32px] py-[40px] relative rounded-[16px] w-[327px] ${isVariant5OrVariant6OrVariant7OrVariant8 ? "opacity-10" : ""}`}>
      {isDefaultOrVariant2OrVariant3OrVariant4OrVariant5OrVariant6Or && (
        <>
          <div className="[word-break:break-word] content-stretch flex flex-col gap-[16px] items-center relative shrink-0 text-center w-full">
            <p className="font-['Manrope:Bold',sans-serif] font-bold leading-[30px] relative shrink-0 text-[#000b21] text-[24px] w-full">Ранний доступ</p>
            <p className="font-['Manrope:Regular',sans-serif] font-normal leading-[24px] relative shrink-0 text-[#666d7a] text-[16px] w-full">Оставьте email или телефон, чтобы получить приглашение и бонус +200 ₽ на первую покупку</p>
          </div>
          <div className="absolute bg-white content-stretch flex h-[40px] items-center justify-center left-[279px] p-[8px] rounded-[24px] top-[16px]" data-name="Close">
            <div className="relative shrink-0 size-[24px]" data-name="Iconly Pack">
              <div className="absolute inset-[11.46%_11.45%_11.46%_11.46%]" data-name="Close Square">
                <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 18.5 18.5">
                  <g id="Close Square">
                    <path d={svgPaths.p1ef16780} id="Stroke 1" stroke="var(--stroke-0, #000B21)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" />
                    <path d={svgPaths.p298c9c80} id="Stroke 2" stroke="var(--stroke-0, #000B21)" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" />
                  </g>
                </svg>
              </div>
            </div>
          </div>
          <div className="content-stretch flex flex-col gap-[16px] items-start relative shrink-0 w-full">
            <div className={`content-stretch flex relative shrink-0 w-full ${isVariant3OrVariant4 ? "flex-col gap-[8px] items-start" : "items-center"}`}>
              {["Default", "Variant2", "Variant5", "Variant6", "Variant7", "Variant8"].includes(property1) && (
                <div className={`flex-[1_0_0] min-w-px relative ${isVariant5OrVariant6OrVariant7OrVariant8 ? "rounded-bl-[8px] rounded-tl-[8px]" : "rounded-[8px]"}`} data-name="Button">
                  <div className={`flex flex-row items-center overflow-clip rounded-[inherit] size-full ${isVariant5OrVariant6OrVariant7OrVariant8 ? "justify-center" : ""}`}>
                    <div className={`content-stretch flex items-center relative size-full ${isVariant5OrVariant6OrVariant7OrVariant8 ? "justify-center px-[24px] py-[8px]" : "p-[16px]"}`}>
                      <div className={`[word-break:break-word] flex flex-col font-["Inter:Regular",sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[16px] whitespace-nowrap ${["Variant2", "Variant5", "Variant6", "Variant7", "Variant8"].includes(property1) ? "text-[#000b21]" : "text-[#999da6]"}`}>
                        <p className="leading-[24px]">{isVariant5OrVariant6OrVariant7OrVariant8 ? "Email" : property1 === "Variant2" ? "vvozhu_enail@mail.ru" : "Введите email"}</p>
                      </div>
                    </div>
                  </div>
                  <div aria-hidden className={`absolute border border-[#e0dfff] border-solid inset-0 pointer-events-none ${isVariant5OrVariant6OrVariant7OrVariant8 ? "rounded-bl-[8px] rounded-tl-[8px]" : "rounded-[8px]"}`} />
                </div>
              )}
              {isVariant5OrVariant6OrVariant7OrVariant8 && (
                <div className="bg-[#6461ff] flex-[1_0_0] min-w-px relative rounded-br-[8px] rounded-tr-[8px]" data-name="Button">
                  <div className="flex flex-row items-center justify-center overflow-clip rounded-[inherit] size-full">
                    <div className="content-stretch flex items-center justify-center px-[24px] py-[8px] relative size-full">
                      <div className="[word-break:break-word] flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[16px] text-white whitespace-nowrap">
                        <p className="leading-[24px]">Телефон</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              {isVariant3OrVariant4 && (
                <>
                  <div className="content-stretch flex items-center relative shrink-0 w-full">
                    <div className="flex-[1_0_0] min-w-px relative rounded-[8px]" data-name="Button">
                      <div className="flex flex-row items-center overflow-clip rounded-[inherit] size-full">
                        <div className="content-stretch flex items-center p-[16px] relative size-full">
                          <div className={`[word-break:break-word] flex flex-col font-["Inter:Regular",sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[16px] whitespace-nowrap ${isVariant4 ? "text-[#999da6]" : "text-[#000b21]"}`}>
                            <p className="leading-[24px]">{isVariant4 ? "Введите email" : isVariant3 ? "vvozhu_enail_mail.ru" : ""}</p>
                          </div>
                        </div>
                      </div>
                      <div aria-hidden className="absolute border border-[#ff4242] border-solid inset-0 pointer-events-none rounded-[8px]" />
                    </div>
                  </div>
                  <p className="[word-break:break-word] font-['Manrope:Regular',sans-serif] font-normal leading-[24px] relative shrink-0 text-[#ff4242] text-[16px] w-full">{isVariant4 ? "Пожалуйста, введите email" : isVariant3 ? "Email указан неверно" : ""}</p>
                </>
              )}
            </div>
            {isVariant5OrVariant6OrVariant7OrVariant8 && (
              <div className={`content-stretch flex relative shrink-0 w-full ${isVariant7OrVariant8 ? "flex-col gap-[8px] items-start" : "items-center"}`}>
                {["Variant5", "Variant6"].includes(property1) && (
                  <div className="flex-[1_0_0] min-w-px relative rounded-[8px]" data-name="Button">
                    <div className="flex flex-row items-center overflow-clip rounded-[inherit] size-full">
                      <div className="content-stretch flex items-center p-[16px] relative size-full">
                        <div className={`[word-break:break-word] flex flex-col font-["Inter:Regular",sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[16px] whitespace-nowrap ${isVariant6 ? "text-[#000b21]" : "text-[#999da6]"}`}>
                          <p className={isVariant6 ? "leading-[24px]" : undefined}>
                            {isVariant5 && (
                              <>
                                <span className="leading-[24px] text-[#000b21]">+7</span>
                                <span className="leading-[24px]">{` (`}</span>
                              </>
                            )}
                            {isVariant6 && "+7 (777) 777-77-77"}
                          </p>
                        </div>
                      </div>
                    </div>
                    <div aria-hidden className="absolute border border-[#e0dfff] border-solid inset-0 pointer-events-none rounded-[8px]" />
                  </div>
                )}
                {isVariant7OrVariant8 && (
                  <>
                    <div className="content-stretch flex items-center relative shrink-0 w-full">
                      <div className="flex-[1_0_0] min-w-px relative rounded-[8px]" data-name="Button">
                        <div className="flex flex-row items-center overflow-clip rounded-[inherit] size-full">
                          <div className="content-stretch flex items-center p-[16px] relative size-full">
                            <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#000b21] text-[16px] whitespace-nowrap">
                              <p className={isVariant7 ? "leading-[24px]" : undefined}>
                                {isVariant7 && "+7 (777) 777-77-77"}
                                {isVariant8 && (
                                  <>
                                    <span className="leading-[24px]">{`+7 `}</span>
                                    <span className="leading-[24px] text-[#999da6]">(</span>
                                  </>
                                )}
                              </p>
                            </div>
                          </div>
                        </div>
                        <div aria-hidden className="absolute border border-[#ff4242] border-solid inset-0 pointer-events-none rounded-[8px]" />
                      </div>
                    </div>
                    <p className="[word-break:break-word] font-['Manrope:Regular',sans-serif] font-normal leading-[24px] relative shrink-0 text-[#ff4242] text-[16px] w-full">{isVariant8 ? "Пожалуйста, введите номер" : isVariant7 ? "Номер указан неверно" : ""}</p>
                  </>
                )}
              </div>
            )}
          </div>
          <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full">
            <div className="bg-[#6461ff] relative rounded-[8px] shrink-0 w-full" data-name="Button">
              <div className="flex flex-row items-center justify-center overflow-clip rounded-[inherit] size-full">
                <div className="content-stretch flex items-center justify-center px-[24px] py-[16px] relative size-full">
                  <div className="[word-break:break-word] flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[16px] text-white whitespace-nowrap">
                    <p className="leading-[24px]">Записаться</p>
                  </div>
                </div>
              </div>
            </div>
            <p className="[word-break:break-word] font-['Manrope:Regular',sans-serif] font-normal leading-[normal] relative shrink-0 text-[#999da6] text-[12px] text-center w-full">Нажимая на кнопку вы соглашаетесь на обработку данных</p>
          </div>
        </>
      )}
      {isVariant9OrVariant10 && (
        <>
          <div className="relative shrink-0 size-[85px]" data-name="image 3651">
            <img alt="" className="absolute inset-0 max-w-none object-cover pointer-events-none size-full" src={isVariant10 ? imgImage3652 : imgImage3651} />
          </div>
          <div className="[word-break:break-word] content-stretch flex flex-col gap-[16px] items-center relative shrink-0 text-center w-full">
            <p className="font-['Manrope:Bold',sans-serif] font-bold leading-[30px] relative shrink-0 text-[#000b21] text-[24px] w-full">{isVariant10 ? "Не удалось отправить заявку" : isVariant9 ? "Заявка принята" : ""}</p>
            <p className="font-['Manrope:Regular',sans-serif] font-normal leading-[24px] relative shrink-0 text-[#666d7a] text-[16px] w-full">{isVariant10 ? "Кажется, произошла ошибка. Попробуйте ещё раз" : isVariant9 ? "Спасибо! Мы добавили вас в список раннего доступа и скоро свяжемся с вами" : ""}</p>
          </div>
          <div className="content-stretch flex flex-col items-start relative shrink-0 w-full">
            <div className="bg-[#6461ff] relative rounded-[8px] shrink-0 w-full" data-name="Button">
              <div className="flex flex-row items-center justify-center overflow-clip rounded-[inherit] size-full">
                <div className="content-stretch flex items-center justify-center px-[24px] py-[16px] relative size-full">
                  <div className="[word-break:break-word] flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[16px] text-white whitespace-nowrap">
                    <p className="leading-[24px]">{isVariant10 ? "Повторить" : isVariant9 ? "Хорошо" : ""}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}