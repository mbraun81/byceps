"""
:Copyright: 2006-2022 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from byceps.services.brand.transfer.models import Brand
from byceps.services.orga_team import service as orga_team_service
from byceps.services.party.transfer.models import Party


def test_teams_for_party(orga_team_admin_client, party: Party) -> None:
    url = f'/admin/orga_teams/teams/{party.id}'
    response = orga_team_admin_client.get(url)
    assert response.status_code == 200


def test_team_create_form(orga_team_admin_client, party: Party) -> None:
    url = f'/admin/orga_teams/teams/{party.id}/create'
    response = orga_team_admin_client.get(url)
    assert response.status_code == 200


def test_team_create_and_delete(orga_team_admin_client, party: Party) -> None:
    assert orga_team_service.count_teams_for_party(party.id) == 0

    url = f'/admin/orga_teams/teams/{party.id}'
    form_data = {'title': 'Support'}
    response = orga_team_admin_client.post(url, data=form_data)
    assert response.status_code == 302
    assert orga_team_service.count_teams_for_party(party.id) == 1

    teams = orga_team_service.get_teams_for_party(party.id)
    assert len(teams) == 1
    team = list(teams)[0]
    url = f'/admin/orga_teams/teams/{team.id}'
    response = orga_team_admin_client.delete(url)
    assert response.status_code == 204
    assert orga_team_service.find_team(team.id) is None
    assert orga_team_service.count_teams_for_party(party.id) == 0


def test_teams_copy_form_with_target_party_teams(
    orga_team_admin_client, brand: Brand, make_party
) -> None:
    source_party = make_party(brand.id)
    target_party = make_party(brand.id)

    team = orga_team_service.create_team(target_party.id, 'Security')

    url = f'/admin/orga_teams/teams/{target_party.id}/copy'
    response = orga_team_admin_client.get(url)
    assert response.status_code == 302

    # Clean up.
    orga_team_service.delete_team(team.id)


def test_teams_copy_form_without_source_teams(
    orga_team_admin_client, brand: Brand, make_party
) -> None:
    target_party = make_party(brand.id)

    url = f'/admin/orga_teams/teams/{target_party.id}/copy'
    response = orga_team_admin_client.get(url)
    assert response.status_code == 302


def test_teams_copy_form_with_source_teams(
    orga_team_admin_client, brand: Brand, make_party
) -> None:
    source_party = make_party(brand.id)
    target_party = make_party(brand.id)

    team = orga_team_service.create_team(source_party.id, 'Tech')

    url = f'/admin/orga_teams/teams/{target_party.id}/copy'
    response = orga_team_admin_client.get(url)
    assert response.status_code == 200

    # Clean up.
    orga_team_service.delete_team(team.id)


def test_teams_copy(orga_team_admin_client, brand: Brand, make_party) -> None:
    source_party = make_party(brand.id)
    target_party = make_party(brand.id)

    team1 = orga_team_service.create_team(source_party.id, 'Support')
    team2 = orga_team_service.create_team(source_party.id, 'Tech')

    assert orga_team_service.count_teams_for_party(source_party.id) == 2
    assert orga_team_service.count_teams_for_party(target_party.id) == 0

    url = f'/admin/orga_teams/teams/{target_party.id}/copy'
    form_data = {'party_id': source_party.id}
    response = orga_team_admin_client.post(url, data=form_data)
    assert response.status_code == 302

    assert orga_team_service.count_teams_for_party(source_party.id) == 2
    assert orga_team_service.count_teams_for_party(target_party.id) == 2

    # Clean up.
    new_teams = orga_team_service.get_teams_for_party(target_party.id)
    for team in {team1, team2}.union(new_teams):
        orga_team_service.delete_team(team.id)
