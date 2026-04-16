interface FunctioningProfilePanelProps {
  text: string;
}

export function FunctioningProfilePanel({
  text,
}: FunctioningProfilePanelProps) {
  return (
    <section className="panel-card overflow-hidden">
      <header className="border-b border-almia-100 bg-gradient-to-r from-[#f6fbfa] to-almia-50 px-6 py-4">
        <h3 className="panel-title text-almia-700">Perfil de funcionamiento</h3>
      </header>
      <div className="p-6">
        <p className="whitespace-pre-line text-[15px] leading-8 text-slate-700">
          {text || "No se recibió descripción detallada del perfil de funcionamiento."}
        </p>
      </div>
    </section>
  );
}
