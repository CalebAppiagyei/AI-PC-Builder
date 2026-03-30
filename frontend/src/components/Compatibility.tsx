
type Props = {
    compatIssues: string;
}

export default function Compatibility({compatIssues}: Props) {
    return (
        <div className="panel">
            <h2 className="panel__title">Compatibility Issues</h2>
            <div className="outputBox" role="status" aria-live="polite">
                <pre className="outputBox__pre">{compatIssues}</pre>
            </div>
        </div>
    )
}