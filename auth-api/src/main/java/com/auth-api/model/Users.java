package com.storefront.model;

import lombok.Data;
import lombok.NonNull;

import java.util.List;
import java.util.UUID;

@Data
public class Users {

    @NonNull
    private String guid;

    @NonNull
    private List<UsersStatusEvent> usersActionsEvents;

    @NonNull
    private List<UsersItem> usersActions;

    public Users() {

        this.guid = UUID.randomUUID().toString();
    }

    public Users(List<UsersStatusEvent> usersStatusEvents, List<UsersItem> usersActions) {

        this.guid = UUID.randomUUID().toString();
        this.usersStatusEvents = usersStatusEvents;
        this.usersItems = usersActions;
    }
}
