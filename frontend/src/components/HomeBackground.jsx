import React from "react";

export default function HomeBackground() {
  const dots = [
    [8, 15],
    [22, 55],
    [92, 10],
    [80, 60],
    [50, 8],
    [96, 85],
    [4, 80],
    [60, 92],
    [35, 35],
    [70, 30],
  ];

  return (
    <div
      className="app-background"
      aria-hidden="true"
    >
      <svg
        viewBox="0 0 100 100"
        preserveAspectRatio="none"
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          opacity: 0.5,
          pointerEvents: "none",
        }}
      >
        {dots.map((d, i) => (
          <circle
            key={i}
            cx={d[0]}
            cy={d[1]}
            r={i % 3 === 0 ? 0.55 : 0.32}
            fill={
              i % 2 === 0
                ? "#FFB35B"
                : "#45E0D0"
            }
            className="cp-dot"
            style={{
              animationDelay: `${i * 0.25}s`,
            }}
          />
        ))}
      </svg>
    </div>
  );
}