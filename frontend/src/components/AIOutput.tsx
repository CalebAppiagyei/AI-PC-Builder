export default function AIOutput({ aiOutput }: any) {
    return (
        <section className="panel">
          <h2 className="panel__title">AI Output</h2>
          <div className="outputBox outputBox--tall">
            <pre className="outputBox__pre">{aiOutput}</pre>
          </div>
        </section>
    )
}