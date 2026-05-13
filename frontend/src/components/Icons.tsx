import type { SVGProps } from "react";

type IconProps = SVGProps<SVGSVGElement>;

export function UploadArrowIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" {...props}>
      <path
        d="M12 16V5"
        strokeWidth="2.2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M7.75 9.25L12 5L16.25 9.25"
        strokeWidth="2.2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M5 19H19"
        strokeWidth="2.2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function PlusIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" {...props}>
      <path
        d="M12 5V19M5 12H19"
        strokeWidth="2.2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function CheckIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" {...props}>
      <path
        d="M5 12.5L10 17.5L19 6.5"
        strokeWidth="2.3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function AlertIcon(props: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" {...props}>
      <path
        d="M12 7V13"
        strokeWidth="2.2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M12 17H12.01"
        strokeWidth="2.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M10.29 3.86L2.82 17.01C2.04 18.38 3.03 20 4.6 20H19.4C20.97 20 21.96 18.38 21.18 17.01L13.71 3.86C12.93 2.49 11.07 2.49 10.29 3.86Z"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
