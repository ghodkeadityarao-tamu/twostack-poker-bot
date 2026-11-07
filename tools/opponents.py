"""Test opponents for in-process self-play. make(name) -> object with the 3 bot functions."""
import random, types, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from game import Action
import bot_core
from game import Street


def _mk(choose, name):
    m = types.SimpleNamespace()
    m.new_half = lambda config, memory: memory.update(rng=random.Random(7), nprng=__import__("numpy").random.default_rng(7))
    m.choose_action = choose
    m.on_hand_end = lambda r, memory: None
    return m


def _rand(obs, mem): return mem["rng"].choice(obs.legal_actions)
def _station(obs, mem): return Action.CHECK_CALL
def _pot(obs, mem): return Action.RAISE_POT if Action.RAISE_POT in obs.legal_actions else Action.CHECK_CALL
def _half(obs, mem): return Action.RAISE_HALF if Action.RAISE_HALF in obs.legal_actions else Action.CHECK_CALL
def _foldy(obs, mem): return Action.CHECK_CALL if obs.to_call == 0 else Action.FOLD


def _eq(obs, mem, n=60):
    if obs.street == Street.PREFLOP:
        return bot_core.preflop_equity(obs.hole_cards)
    return bot_core.np_equity(obs.hole_cards, obs.board, 500, mem["nprng"])


def make_eqbot(call_margin, raise_eq, bet_eq, bluff=0.0):
    def f(obs, mem):
        eq = _eq(obs, mem)
        legal = obs.legal_actions
        c, pot = obs.to_call, obs.pot
        if c > 0:
            need = c / (pot + c)
            if eq < need + call_margin:
                return Action.FOLD
            if eq > raise_eq and Action.RAISE_POT in legal:
                return Action.RAISE_POT
            return Action.CHECK_CALL
        if eq > bet_eq and Action.RAISE_POT in legal:
            return Action.RAISE_POT
        if bluff and Action.RAISE_HALF in legal and mem["rng"].random() < bluff:
            return Action.RAISE_HALF
        return Action.CHECK_CALL
    return f


FACTORY = {
    "random": _rand, "station": _station, "pot": _pot, "half": _half, "foldy": _foldy,
    "tight": make_eqbot(0.05, 0.70, 0.64),
    "loose": make_eqbot(0.0, 0.62, 0.55, 0.2),
    "nit": make_eqbot(0.10, 0.75, 0.70),
    "maniac": make_eqbot(-0.05, 0.5, 0.5, 0.5),
}


def make(name):
    return _mk(FACTORY[name], name)


def _randagg(obs, mem):
    r = mem["rng"].random(); legal = obs.legal_actions
    if r < 0.45 and Action.RAISE_POT in legal: return Action.RAISE_POT
    if r < 0.60 and Action.RAISE_HALF in legal: return Action.RAISE_HALF
    if obs.to_call > 0 and r > 0.85: return Action.FOLD
    return Action.CHECK_CALL


def _overfold(obs, mem):
    # calls small bets, folds to anything big; bets only with strong hands
    eq = _eq(obs, mem)
    if obs.to_call > 0:
        return Action.CHECK_CALL if obs.to_call <= 0.3 * obs.pot and eq > .4 else Action.FOLD
    return Action.RAISE_HALF if eq > 0.6 and Action.RAISE_HALF in obs.legal_actions else Action.CHECK_CALL


FACTORY["randagg"] = _randagg
FACTORY["overfold"] = _overfold
