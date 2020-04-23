package com.storefront.model;

import lombok.Data;
import lombok.NonNull;

import java.sql.Timestamp;

@Data
public class UsersStatusEvent {

    @NonNull
    private Long timestamp;

    @NonNull
    private UsersStatusType usersStatusType;

    private String note;

    public UsersStatusEvent() {

        this.timestamp = new Timestamp(System.currentTimeMillis()).getTime();
    }

    public UsersStatusEvent(UsersStatusType usersStatusType) {

        this.timestamp = new Timestamp(System.currentTimeMillis()).getTime();
        this.usersStatusType = usersStatusType;
    }

    public UsersStatusEvent(UsersStatusType usersStatusType, String note) {

        this.timestamp = new Timestamp(System.currentTimeMillis()).getTime();
        this.usersStatusType = usersStatusType;
        this.note = note;
    }
}

