from api.shared.password_hasher import PasswordHasher


if __name__ == "__main__":
    password = "123"
    hashed_password = PasswordHasher.hash(password)
    print(f"Hashed password ({password}): {hashed_password}")

    is_valid = PasswordHasher.verify(password, hashed_password)
    print(f"Password valid: {is_valid}")


    is_valid = PasswordHasher.verify('123', '$2b$12$IEW4mqNtZBcL4ZucJ1g3Re9elKCInfEr5trGGvpBtknHXsWu1M1pq')
    print(f"Password valid after db reading: {is_valid}")
    is_valid = PasswordHasher.verify('123', '$2b$12$OK.pmNvzeXNsmhR4LK/adeUB1Y0G3ZOwj5aQiUKkclBlnyAulyh4m')
    print(f"Password valid after copying and pasting the value from directly from the db: {is_valid}")
    
