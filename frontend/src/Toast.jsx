// Sistema de notificaciones (toasts) sin dependencias. Cualquier componente llama
// a useToast()("mensaje", "ok"|"info"|"error") y aparece abajo, se va solo.
import { createContext, useCallback, useContext, useState } from "react";
import Icon from "./Icon.jsx";

const ToastCtx = createContext(() => {});
export const useToast = () => useContext(ToastCtx);

let idSeq = 0;
const ICONO = { ok: "check-circle", info: "info", error: "x-circle" };

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const notificar = useCallback((mensaje, tipo = "ok") => {
    const id = ++idSeq;
    setToasts((t) => [...t, { id, mensaje, tipo }]);
    setTimeout(() => setToasts((t) => t.filter((x) => x.id !== id)), 3400);
  }, []);

  return (
    <ToastCtx.Provider value={notificar}>
      {children}
      <div className="toaster">
        {toasts.map((t) => (
          <div key={t.id} className={"toast " + t.tipo} role="status">
            <Icon name={ICONO[t.tipo] || "info"} size={18} />
            <span>{t.mensaje}</span>
          </div>
        ))}
      </div>
    </ToastCtx.Provider>
  );
}
