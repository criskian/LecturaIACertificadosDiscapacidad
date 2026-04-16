interface DisabilityBadgeProps {
  label: string;
  prominent?: boolean;
  cardLike?: boolean;
}

export function DisabilityBadge({
  label,
  prominent = false,
  cardLike = false,
}: DisabilityBadgeProps) {
  return (
    <span
      className={[
        "inline-flex items-center font-bold transition",
        cardLike
          ? "min-h-[92px] rounded-[24px] border border-almia-200 bg-gradient-to-br from-white via-almia-50 to-almia-100/70 px-4 py-4 text-left text-almia-800 shadow-sm"
          : prominent
            ? "rounded-full bg-almia-400 px-4 py-2 text-sm text-white shadow-sm shadow-almia-400/20"
            : "rounded-full border border-almia-200 bg-almia-50 px-4 py-2 text-sm text-almia-700",
      ].join(" ")}
    >
      {cardLike ? (
        <span className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-almia-400 text-xs font-extrabold uppercase tracking-[0.18em] text-white">
            Act
          </span>
          <span className="text-sm font-extrabold uppercase tracking-[0.12em]">
            {label}
          </span>
        </span>
      ) : (
        label
      )}
    </span>
  );
}
