export interface GameData {
  id: number;
  name: string;
  description: string;
  price: number;
  image: string;
  link: string;
  pc_requirements: Record<string, string>;
  mac_requirements: Record<string, string>;
  linux_requirements: Record<string, string>;
  genres: Array< string >;
  categories: Array< string >;
}