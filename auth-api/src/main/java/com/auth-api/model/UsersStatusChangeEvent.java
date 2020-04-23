package com.storefront.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UsersStatusChangeEvent {

    @NonNull
    private String guid;

    @NonNull
    private UsersStatusEvent usersStatusEvent;

}
