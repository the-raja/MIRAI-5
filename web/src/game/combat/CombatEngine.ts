export type ActionType =
  | 'BasicAttack'
  | 'HeavyAttack'
  | 'Dash'
  | 'Heal'
  | 'Ultimate'
  | 'Death';

export interface EntityState {
  x: number;
  y: number;
  hp: number;
  maxHp: number;
  stamina: number;
  ultimateCharge: number;
  currentAction: ActionType | 'Idle';
}

export class CombatEngine {
  public playerState: EntityState = {
    x: -5,
    y: 0,
    hp: 100,
    maxHp: 100,
    stamina: 100,
    ultimateCharge: 0,
    currentAction: 'Idle',
  };

  public bossState: EntityState = {
    x: 5,
    y: 0,
    hp: 100,
    maxHp: 100,
    stamina: 100,
    ultimateCharge: 50,
    currentAction: 'Idle',
  };

  public processPlayerAction(action: ActionType): { damageDealt: number; damageTaken: number } {
    this.playerState.currentAction = action;
    let dmgDealt = 0;
    let dmgTaken = 0;

    switch (action) {
      case 'BasicAttack':
        dmgDealt = 12;
        this.playerState.ultimateCharge = Math.min(100, this.playerState.ultimateCharge + 10);
        break;
      case 'HeavyAttack':
        dmgDealt = 28;
        this.playerState.ultimateCharge = Math.min(100, this.playerState.ultimateCharge + 25);
        break;
      case 'Dash':
        this.playerState.x += 2;
        break;
      case 'Heal':
        this.playerState.hp = Math.min(100, this.playerState.hp + 30);
        break;
      case 'Ultimate':
        if (this.playerState.ultimateCharge >= 100) {
          dmgDealt = 55;
          this.playerState.ultimateCharge = 0;
        }
        break;
      case 'Death':
        this.playerState.hp = 0;
        break;
    }

    if (dmgDealt > 0) {
      this.bossState.hp = Math.max(0, this.bossState.hp - dmgDealt);
    }

    return { damageDealt: dmgDealt, damageTaken: dmgTaken };
  }
}
