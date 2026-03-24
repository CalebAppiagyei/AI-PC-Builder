type Props = {
  query: string;
  setQuery: (q: string) => void;
  options: {label: string, value: string}[];
  onSelect: (lable: string, value: string) => void;
}

export default function AutoComplete({ query, setQuery, options, onSelect }: Props) {
    return  (
        <>
            <input 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder='Search...' />
            <div>
                {options.map((option) => (
                    <button key={option.value} onClick={() => onSelect(option.value, option.label)}>
                        { option.label }
                    </button>
                ))}
            </div>
        </>
    )
}