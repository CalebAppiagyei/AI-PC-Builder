type AIOutputProps = {
  aiOutput: string
}


export default function AIOutput({ aiOutput }: AIOutputProps) {
    return (
        <section className="panel">
          {/* Bottom */}
          <h2 className="panel__title">AI Output</h2>
          <div className="outputBox outputBox--tall">
            <pre className="outputBox__pre">{aiOutput}</pre>
          </div>
        </section>
    )
}