import React from "react";
import {
  Mic,
  CheckCircle2,
} from "lucide-react";

export default function HomePreview() {
  return (
    <div
      className="cp-preview"
      style={{
        width: "100%",
        maxWidth: 460,

        padding: 26,

        borderRadius: 26,

        background: "rgba(255,255,255,0.06)",

        border:
          "1px solid rgba(255,255,255,0.14)",

        backdropFilter: "blur(18px)",
        WebkitBackdropFilter: "blur(18px)",

        boxShadow:
          "0 30px 70px -30px rgba(0,0,0,0.65)",

        position: "relative",
      }}
    >

      {/* HEADER */}

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >

        <span
          className="cp-mono"
          style={{
            fontSize: 11,
            letterSpacing: "0.1em",
            color: "#C2C4EC",
          }}
        >
          LIVE SESSION
        </span>

        <div
          style={{
            display: "flex",
            gap: 7,
          }}
        >
          <i
            style={{
              width: 8,
              height: 8,
              borderRadius: "50%",
              background: "#FF8270",
            }}
          />

          <i
            style={{
              width: 8,
              height: 8,
              borderRadius: "50%",
              background: "#FFB35B",
            }}
          />

          <i
            style={{
              width: 8,
              height: 8,
              borderRadius: "50%",
              background: "#45E0D0",
            }}
          />
        </div>

      </div>


      {/* QUESTION */}

      <div
        style={{
          display: "flex",
          gap: 14,
          alignItems: "flex-start",
          marginTop: 28,
        }}
      >

        <div
          style={{
            width: 42,
            height: 42,

            borderRadius: 12,

            background:
              "rgba(255,179,91,0.12)",

            display: "flex",
            alignItems: "center",
            justifyContent: "center",

            flexShrink: 0,
          }}
        >
          <Mic
            size={18}
            color="#FFB35B"
          />
        </div>


        <div
          style={{
            flex: 1,

            padding: "14px 16px",

            borderRadius: 14,

            background:
              "rgba(139,124,246,0.13)",

            color: "#FBFAFF",

            fontSize: 13,

            lineHeight: 1.5,
          }}
        >
          "Tell me about a time you handled conflict on a team."
        </div>

      </div>


      {/* ANSWER */}

      <div
        style={{
          display: "flex",
          gap: 10,
          alignItems: "center",
          marginTop: 18,
        }}
      >

        <div
          style={{
            flex: 1,

            padding: "13px 16px",

            border:
              "1px solid rgba(69,224,208,0.35)",

            borderRadius: 14,

            color: "#C2C4EC",

            fontSize: 13,

            lineHeight: 1.5,
          }}
        >
          "On my last team, a teammate and I disagreed on scope, so I..."
        </div>

        <span
          style={{
            background: "#45E0D0",

            padding: "7px 10px",

            borderRadius: 9,

            fontSize: 11,

            color: "#191C36",

            fontWeight: 600,
          }}
        >
          You
        </span>

      </div>


      {/* DIVIDER */}

      <div
        style={{
          height: 1,

          background:
            "rgba(255,255,255,0.10)",

          margin: "25px 0",
        }}
      />


      {/* SCORE */}

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 15,
        }}
      >

        <div
          style={{
            width: 68,
            height: 68,

            borderRadius: "50%",

            border:
              "5px solid #FFB35B",

            display: "flex",
            alignItems: "center",
            justifyContent: "center",

            flexShrink: 0,
          }}
        >
          <strong
            style={{
              fontSize: 13,
              color: "#FBFAFF",
            }}
          >
            78%
          </strong>
        </div>


        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 4,
          }}
        >

          <strong
            className="cp-display"
            style={{
              fontSize: 16,
              color: "#FBFAFF",
            }}
          >
            78% ready
          </strong>

          <span
            style={{
              fontSize: 11,
              color: "#C2C4EC",
            }}
          >
            Clarity + structure score
          </span>

        </div>


        <div
          style={{
            marginLeft: "auto",

            display: "flex",
            alignItems: "center",
            gap: 5,

            fontSize: 11,

            color: "#45E0D0",
          }}
        >
          <CheckCircle2 size={13} />
          On track
        </div>

      </div>

    </div>
  );
}