export interface SpiritPower {
  name: string
  description: string
  tags: string[]
  weakness_tag: string
  specializations: string[]
}

export interface BasicInfo {
  name: string
  codename: string
  gender: string
  age: string
  bond: string
  karma_tags: string[]
  backstory: string
  appearance: string
  experience_tags: string[]
}

export interface Attributes {
  physique: string
  wisdom: string
  spirit: string
}

export interface Resources {
  hp_max: number
  hp_current: number
  spirit_power_max: number
  spirit_power_current: number
  stylish_points: number
  item_points: number
  exp: number
  spirit_awareness: number
}

export interface SkillEntry {
  attribute_bonus: number
  free_points: number
}

export interface Skills {
  athletics: SkillEntry
  operation: SkillEntry
  stealth: SkillEntry
  investigation: SkillEntry
  insight: SkillEntry
  persuasion: SkillEntry
  hunter_lore: SkillEntry
}

export interface CharacterCard {
  spirit_power: SpiritPower
  basic_info: BasicInfo
  attributes: Attributes
  resources: Resources
  skills: Skills
  martial_arts: any[]
  spells: any[]
  spirit_marks: any[]
  soul_weapon: any | null
  ultimates: any[]
  feats: any[]
  stylish_moves: any[]
}

export interface ValidationResult {
  valid: boolean
  errors: string[]
  warnings: string[]
  unlocked: Record<string, any>
}

export interface CreationSession {
  id: string
  current_step: number
  character: CharacterCard
  completed_steps: number[]
  validation_results: Record<number, ValidationResult>
}
