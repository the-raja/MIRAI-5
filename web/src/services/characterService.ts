import charactersData from '@/data/characters.json';

export interface Character {
  id: string;
  name: string;
  role: string;
  voice: string;
  abilities: string[];
  animations: string[];
  portrait: string;
  model: string;
  ultimate: string;
  description: string;
}

export class CharacterService {
  public static getAllCharacters(): Character[] {
    return charactersData as Character[];
  }

  public static getCharacterByName(name: string): Character {
    const found = charactersData.find((c) => c.name.toLowerCase() === name.toLowerCase());
    return (found as Character) || (charactersData[0] as Character);
  }
}
