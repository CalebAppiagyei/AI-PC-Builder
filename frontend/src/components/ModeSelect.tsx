// set types for Mode avoid to use any type and read/write bug
import type { Mode } from "../types"
type ModeProps = {
  mode: Mode;
  setMode: React.Dispatch<React.SetStateAction<Mode>>;
};

export default function ModeSelect({mode, setMode}: ModeProps) {
    return (
        <section className="modeRow">
        {/* Toggle row */}
          <div className="toggle">
            <button
              className={mode === "full" ? "toggle__btn toggle__btn--active" : "toggle__btn"}
              onClick={() => setMode("full")}
              type="button"
            >
              Full PC Build
            </button>
            <button
              className={mode === "upgrade" ? "toggle__btn toggle__btn--active" : "toggle__btn"}
              onClick={() => setMode("upgrade")}
              type="button"
            >
              Upgrade Recommendation
            </button>
          </div>
        </section>
    )
}