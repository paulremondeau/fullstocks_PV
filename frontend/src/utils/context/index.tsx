import { createContext } from "react";

export interface AvailableData {
    [key: number]: { [key: string]: string | number }
}

export interface SystemInterface {
    "info": any[],
    "monthly_chart": { "data": any[], "layout": {} },
    "daily_chart": { "data": any[], "layout": {} },
}

export const AvailableDataContext = createContext<AvailableData>({});
export const SystemContext = createContext<SystemInterface>({
    "info": [],
    "monthly_chart": { "data": [], "layout": {} },
    "daily_chart": { "data": [], "layout": {} },
})

interface SelectedSystemInterface {
    [key: string]: string | number
}

interface SelectedSystemContextInterface {
    selectedSystem: SelectedSystemInterface,
    setSelectedSystem: React.Dispatch<React.SetStateAction<{}>>
}

export const SelectSystemContext = createContext<SelectedSystemContextInterface>({
    selectedSystem: {},
    setSelectedSystem: () => { }
});
